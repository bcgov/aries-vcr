import jsonschema
import logging

from api_v2.models.CredentialType import CredentialType
from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema

from api.auth import create_issuer_user, verify_signature, VerifierException

from api_v2.jsonschema.issuer import ISSUER_JSON_SCHEMA


class IssuerException(Exception):
    pass


class IssuerManager:
    """
    Handle registration of issuer services, taking the JSON definition
    of the issuer and updating the related tables.
    """

    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def register_issuer(self, request, spec):
        try:
            jsonschema.validate(spec, ISSUER_JSON_SCHEMA)
        except jsonschema.ValidationError as e:
            raise IssuerException("Schema validation error: {}".format(e))

        # TODO: move sig verification into middleware – decorator?
        try:
            verified = verify_signature(request)
        except VerifierException as e:
            raise IssuerException("Signature validation error: {}".format(e))
        if not verified:
            raise IssuerException("Missing HTTP Signature")
        self.__logger.debug("DID signature verified: %s", verified)

        user = self.update_user(verified, spec["issuer"])
        issuer = self.update_issuer(spec["issuer"])
        schemas, credential_types = self.update_schemas_and_ctypes(
            spec["issuer"], spec.get("credential-types", [])
        )

        result = {
            "issuer": {
                "id": issuer.id,
                "did": issuer.did,
                "name": issuer.name,
                "abbreviation": issuer.abbreviation,
                "email": user.email,
                "url": issuer.url,
            },
            "schemas": [
                {
                    "id": schema.id,
                    "name": schema.name,
                    "version": schema.version,
                    "publisher_did": schema.publisher_did,
                }
                for schema in schemas
            ],
            "credential_types": [
                {
                    "id": credential_type.id,
                    "schema": credential_type.schema.id,
                    "issuer": credential_type.issuer.id,
                    "description": credential_type.description,
                    "processor_config": credential_type.processor_config,
                }
                for credential_type in credential_types
            ],
        }
        return result

    def update_user(self, verified, issuer_def):
        """
        Update Django user with incoming issuer data.
        """
        issuer_did = issuer_def["did"].strip()
        display_name = issuer_def["name"].strip()
        user_email = issuer_def["email"].strip()
        verified_did = verified["keyId"]
        verkey = verified["key"]
        assert "did:sov:{}".format(issuer_did) == verified_did
        return create_issuer_user(
            user_email, verified_did, last_name=display_name, verkey=verkey
        )

    def update_issuer(self, issuer_def):
        """
        Update issuer record if exists, otherwise create.
        """
        issuer_did = issuer_def["did"].strip()
        issuer_name = issuer_def["name"].strip()
        issuer_abbreviation = issuer_def["abbreviation"].strip() or None
        issuer_email = issuer_def["email"].strip() or None
        issuer_url = issuer_def["url"].strip() or None

        issuer, created = Issuer.objects.get_or_create(did=issuer_did)
        issuer.name = issuer_name
        issuer.abbreviation = issuer_abbreviation
        issuer.email = issuer_email
        issuer.url = issuer_url
        issuer.save()

        return issuer

    def update_schemas_and_ctypes(self, issuer, credential_type_defs):
        """
        Update schema records if they exist, otherwise create.
        Create related CredentialType records.
        """

        schemas = []
        credential_types = []

        for credential_type_def in credential_type_defs:
            # Get or create schema
            schema_name = credential_type_def["name"].strip()
            schema_version = credential_type_def["version"].strip()
            schema_publisher_did = issuer.did

            schema, _ = Schema.objects.get_or_create(
                name=schema_name,
                version=schema_version,
                publisher_did=schema_publisher_did,
            )
            schema.save()
            schemas.append(schema)

            # Get or create credential type

            credential_type_description = (
                credential_type_def["description"].strip() or None
            )
            credential_type_processor_config = (
                credential_type_def["mapping"].strip() or None
            )
            credential_type, _ = CredentialType.objects.get_or_create(
                schema=schema, issuer=issuer
            )

            credential_type.description = credential_type_description
            credential_type.processor_config = credential_type_processor_config
            credential_type.save()
            credential_types.append(credential_type)

        return schemas, credential_types
