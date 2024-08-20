import logging
from typing import Sequence, Union

from api.v2.models.CredentialType import CredentialType
from api.v2.models.Schema import Schema

LOGGER = logging.getLogger(__name__)


class CredentialTypeManager:
    """
    Manage the creation and updating of CredentialType and Schema records.
    """

    def update_credential_types(
        self, issuer, schemas, credential_type_defs
    ) -> Sequence[CredentialType]:
        """
        Create related CredentialType records.
        """

        credential_types = []

        for credential_type_def in credential_type_defs:

            # Find the schema for this credential type in schemas
            schema = self._find_matching_schema(issuer, schemas, credential_type_def)

            # Get or create credential type
            credential_type, _ = CredentialType.objects.get_or_create(
                schema=schema, issuer=issuer
            )

            credential_type.processor_config = self._build_processor_config(
                credential_type_def
            )
            credential_type.credential_title = credential_type_def.get(
                "credential_title"
            )
            credential_type.description = credential_type_def.get("name")
            # TODO: Change this to schema_labels
            credential_type.schema_label = credential_type_def.get("labels")
            credential_type.category_labels = credential_type_def.get("category_labels")
            credential_type.claim_labels = credential_type_def.get("claim_labels")
            credential_type.claim_descriptions = credential_type_def.get(
                "claim_descriptions"
            )
            credential_type.logo_b64 = credential_type_def.get("logo_b64")
            credential_type.url = credential_type_def.get("endpoint")

            # TODO: Change this to verification_methods
            credential_type.credential_def_id = credential_type_def.get(
                "credential_def_id"
            )
            credential_type.highlighted_attributes = credential_type_def.get(
                "highlighted_attributes"
            )
            visible_fields = credential_type_def.get("visible_fields")
            if isinstance(visible_fields, list):
                visible_fields = ",".join(
                    x.strip() for x in filter(None, visible_fields)
                )
            credential_type.visible_fields = (
                visible_fields if isinstance(visible_fields, str) else None
            )

            credential_type.save()
            credential_types.append(credential_type)

        return credential_types

    def _find_matching_schema(
        self, issuer, schemas, credential_type_def
    ) -> Union[Schema, None]:
        """
        Find the schema that matches the credential type definition.
        """

        for schema in schemas:
            if (
                schema.name == credential_type_def.get("schema")
                and schema.version == credential_type_def.get("version")
                and schema.origin_did == issuer.did
            ):
                return schema
        return None

    def _build_processor_config(self, credential_type_def):
        processor_config = {
            "cardinality_fields": credential_type_def.get("cardinality_fields"),
            "credential": credential_type_def.get("credential"),
            "mappings": credential_type_def.get("mappings"),
            "topic": credential_type_def.get("topic"),
        }

        return processor_config
