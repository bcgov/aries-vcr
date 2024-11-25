import base64
from datetime import datetime
import hashlib
import logging
import re

from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

from jsonpath_ng import parse

from api.v2.models import (
    Attribute,
    Credential,
    CredentialSet,
    CredentialType,
    Issuer,
    Schema,
    Topic,
)

from agent_webhooks.enums import FormatEnum
from agent_webhooks.schemas import CredentialDefSchema

LOGGER = logging.getLogger(__name__)

# For now this is kept separate from the legacy CredentialManager since there is
# a lot of logic specific to the AnonCreds format there. Eventually we can try
# to make these more generic so it can be used across formats.

format = FormatEnum.VC_DI.value


class CredentialException(Exception):
    pass


class CredentialManager:
    f"""Manage the creation and updating of {format} Credential records."""

    def update_credential(self, credential_def: CredentialDefSchema) -> Credential:
        f"""Update a {format} credential in the database if it exists, otherwise create it."""

        # Get the credential type from the data
        credential_type = self._resolve_credential_type(credential_def)
        processor_config = credential_type.processor_config

        # Resolve the topic for the credential
        topic = self._resolve_credential_topic(credential_def, processor_config)

        # Resolve the cardinality for the credential
        cardinality = self._process_credential_cardinality(
            credential_def, processor_config
        )

        # Resolve the credential properties
        credential_properties = self._process_credential_properties(
            credential_def, processor_config
        )

        # Need this in a separate method for testing
        self._set_additional_properties(credential_def, credential_properties)

        # Set our own credential properties
        credential_properties["credential_type"] = credential_type
        credential_properties["cardinality_hash"] = (
            cardinality["hash"] if cardinality else None
        )

        # Update the database with the credential data
        credential = topic.credentials.create(**credential_properties)

        # Update the credential set
        self._resolve_credential_set(credential, cardinality)

        credential_attributes = self._process_credential_attributes(
            credential_def, processor_config
        )
        for credential_attribute in credential_attributes:
            Attribute.objects.create(**credential_attribute, credential=credential)

        return credential

    def _set_additional_properties(self, credential_def, credential_properties):
        credential_properties["format"] = credential_def.get("format")
        credential_properties["raw_data"] = credential_def.get("raw_data")

    def _resolve_credential_type(
        self, credential_def: CredentialDefSchema
    ) -> CredentialType:
        """Get the credential type based on the credential data."""

        # Get the credential type from the data
        try:
            origin_did = credential_def.get("origin_did")
            name = credential_def.get("schema")
            version = credential_def.get("version")

            issuer = Issuer.objects.get(did=origin_did)
            schema = Schema.objects.get(
                origin_did=origin_did,
                name=name,
                version=version,
            )
        except Issuer.DoesNotExist:
            raise CredentialException(
                "Issuer with" + f" did '{origin_did}' " + "does not exist."
            )
        except Schema.DoesNotExist:
            raise CredentialException(
                "Schema with"
                + f" origin_did '{origin_did}', name '{name}', and version '{version}' "
                + "does not exist."
            )

        return CredentialType.objects.get(schema=schema, issuer=issuer)

    def _resolve_credential_topic(
        self, credential_def: CredentialDefSchema, processor_config: any
    ) -> Topic:
        f"""Resolve the topic for a {format} credential based on the processor config"""

        topic_def = processor_config.get("topic")
        topic_source_id = self._process_mapping(
            topic_def.get("source_id"), credential_def
        )
        topic_type = topic_def.get("type")

        # Throw an error if the topic source_id or type is not provided
        if not topic_source_id or not topic_type:
            raise CredentialException(
                (
                    "Topic source_id or type could not be determined from the processor config.",
                )
            )

        try:
            return Topic.objects.get(source_id=topic_source_id, type=topic_type)
        except Topic.DoesNotExist:
            raise CredentialException(
                f"Topic with source_id '{topic_source_id}' and type '{topic_type}' does not exist."
            )

    def _resolve_credential_set(
        self,
        credential: Credential,
        cardinality: dict = None,
    ) -> CredentialSet:
        if credential.credential_set:
            return credential.credential_set

        query = {
            "cardinality_hash": cardinality.get("hash") if cardinality else None,
            "credential_type": credential.credential_type,
            "topic": credential.topic,
        }

        try:
            credential_set = CredentialSet.objects.get(**query)
            # Assume the credential is the latest until proven otherwise
            latest_credential = credential

            ordered_credentials: list[Credential] = credential_set.credentials.filter(
                revoked=False
            ).order_by("effective_date")

            for last_credential in ordered_credentials:
                if last_credential.effective_date <= credential.effective_date:
                    last_credential.latest = False
                    last_credential.revoked = True
                    last_credential.revoked_by = credential
                    last_credential.revoked_date = credential.effective_date
                    last_credential.save()
                else:
                    latest_credential = last_credential
                    if not credential.revoked:
                        credential.revoked = True
                        credential.revoked_by = last_credential
                        credential.revoked_date = last_credential.effective_date

            # Update the credential set with the latest credential
            credential_set.latest_credential = latest_credential
            # Update the first effective date based on the earliest credential
            credential_set.first_effective_date = (
                credential.effective_date
                if credential_set.first_effective_date is None
                else min(credential_set.first_effective_date, credential.effective_date)
            )

            # Update the last effective date based on the revoked date of the latest credential
            if latest_credential.revoked:
                credential_set.last_effective_date = (
                    (
                        latest_credential.revoked_date
                        if credential_set.last_effective_date is None
                        else max(
                            credential_set.last_effective_date,
                            latest_credential.revoked_date,
                        )
                    )
                    if latest_credential.revoked_date
                    else None
                )
            else:
                credential_set.last_effective_date = None

            credential_set.save()

            # Update the credential with the credential set
            credential.credential_set = credential_set
            credential.latest = latest_credential == credential
            credential.save()

            # Update the latest credential in the set
            if latest_credential != credential and not latest_credential.latest:
                latest_credential.latest = True
                latest_credential.save()

        except CredentialSet.DoesNotExist:
            credential_set = CredentialSet.objects.create(
                **{
                    **query.copy(),
                    "first_effective_date": credential.effective_date,
                    "last_effective_date": (
                        credential.revoked_date if credential.revoked else None
                    ),
                    "latest_credential": credential,
                }
            )

            # Update the credential with the credential set
            credential.credential_set = credential_set
            credential.latest = True
            credential.save()

        return credential_set

    def _process_credential_properties(
        self, credential_def: CredentialDefSchema, processor_config: any
    ) -> dict:
        """
        Generate a dictionary of additional credential properties from the processor config
        """

        if config := processor_config and processor_config.get("credential"):
            effective_date = self._process_config_date(
                config, credential_def, "effective_date"
            )
            revoked_date = self._process_config_date(
                config, credential_def, "revoked_date"
            )

            if revoked_date and revoked_date > datetime.now(timezone.utc).replace(
                tzinfo=timezone.utc
            ):
                # raise CredentialException(
                #     f"Credential revoked_date must be in the past, not: {revoked_date}"
                # )
                # For now, just log a warning and set revoked_date to None
                LOGGER.warning(
                    f"Credential revoked_date must be in the past, not: {revoked_date}"
                )
                revoked_date = None

            return {
                "credential_id": credential_def.get("credential_id"),
                "effective_date": effective_date,
                "revoked_date": revoked_date,
                "revoked": bool(revoked_date),
            }

        return {}

    def _process_credential_cardinality(
        self, credential_def: CredentialDefSchema, processor_config: any
    ) -> any:
        """Extract the credential cardinality values and hash"""

        cardinality = processor_config.get("cardinality") or []
        values = {}
        if cardinality and len(cardinality):
            for attribute in cardinality:
                path = attribute.get("path")
                try:
                    values[path] = self._process_mapping(attribute, credential_def)
                except AttributeError:
                    raise CredentialException(
                        "Processor config specifies field '{}' in cardinality, "
                        + "but value does not exist in credential.".format(path)
                    )
        if values:
            hash_paths = ["{}::{}".format(k, values[k]) for k in values]
            hash = base64.b64encode(
                hashlib.sha256(",".join(hash_paths).encode("utf-8")).digest()
            )
            return {"values": values, "hash": hash}

        return None

    def _process_credential_attributes(
        self, credential_def: CredentialDefSchema, processor_config: dict
    ) -> list[dict]:
        """Generate a dictionary of credential attributes from the processor config"""

        attributes = []
        if config := processor_config and processor_config.get("mappings"):
            for attribute in config:
                attribute_type = attribute.get("type")
                attribute_value = self._process_mapping(attribute, credential_def)
                attributes.append(
                    {
                        "type": attribute_type,
                        "value": attribute_value,
                    }
                )

        return attributes

    def _process_mapping(self, rule: dict, credential_def: CredentialDefSchema) -> any:
        """Takes our mapping rules and returns a value from the credential data."""

        if not (raw_data := credential_def and credential_def.get("raw_data")):
            return None

        if path := rule and rule.get("path"):
            json_path = parse(path)
            matches = [match.value for match in json_path.find(raw_data)]
            return matches[0] if matches and len(matches) else None

        return None

    def _process_config_date(
        self, config: dict, credential_def: CredentialDefSchema, field: str
    ) -> datetime:
        """Process a date field from the processor config."""

        parsed_date = None
        if date_value := self._process_mapping(config.get(field), credential_def):
            # if date_value:
            try:
                # Could be seconds since epoch
                parsed_date = datetime.fromtimestamp(int(date_value), tz=timezone.utc)
            except ValueError:
                # Django method to parse a date string. Must be in ISO8601 format
                try:
                    if not (
                        parsed_date := parse_datetime(date_value)
                        or parse_date(date_value)
                    ):
                        raise ValueError()
                    parsed_date = datetime.combine(parsed_date, datetime.min.time())
                    parsed_date = timezone.make_aware(parsed_date)
                except re.error:
                    raise CredentialException(f"Error parsing {field}: {date_value}")
                except ValueError:
                    raise CredentialException(
                        f"Credential {field} is invalid: {date_value}"
                    )

            if not parsed_date.tzinfo:
                # Interpret as UTC
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            else:
                #  Convert to UTC
                parsed_date = parsed_date.astimezone(timezone.utc)

        return parsed_date
