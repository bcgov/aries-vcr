import logging
from typing import Sequence, Tuple

from api_v2.auth import create_issuer_user
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.serializers.rest import (
    CredentialTypeExtSerializer,
    IssuerSerializer,
    SchemaSerializer,
)

LOGGER = logging.getLogger(__name__)


class IssuerManagerException(Exception):
    """Base exception for issuer manager issues."""


class IssuerRegistrationResult:
    """Model to represent the result of issuer registration."""

    def __init__(
        self,
        issuer: Issuer,
        schemas: Sequence[Schema],
        credential_types: Sequence[CredentialType],
    ):
        """Initialize the issuer registration result instance."""
        self.issuer = issuer
        self.schemas = schemas
        self.credential_types = credential_types

    def serialize(self) -> dict:
        """Serialize to JSON-compatible dict format."""
        return {
            "issuer": IssuerSerializer(self.issuer).data,
            "schemas": [SchemaSerializer(schema).data for schema in self.schemas],
            "credential_types": [
                CredentialTypeExtSerializer(credential_type).data
                for credential_type in self.credential_types
            ],
        }


class IssuerManager:
    """
    Handle registration of issuer services, taking the JSON definition
    of the issuer and updating the related tables.
    """

    def register_issuer(self, spec) -> IssuerRegistrationResult:
        """
        Perform issuer registration, updating the related database models.
        """
        issuer_registration = spec["issuer_registration"]
        issuer = issuer_registration["issuer"]
        self.update_user(issuer)
        issuer = self.update_issuer(issuer_registration["issuer"])
        schemas, credential_types = self.update_schemas_and_ctypes(
            issuer, issuer_registration.get("credential_types", [])
        )
        return IssuerRegistrationResult(issuer, schemas, credential_types)

    def update_user(self, issuer_def):
        """
        Update Django user with incoming issuer data.
        """
        issuer_did = issuer_def["did"]
        display_name = issuer_def["name"]
        user_email = issuer_def["email"]
        return create_issuer_user(user_email, issuer_did, display_name=display_name)

    def update_issuer(self, issuer_def) -> Issuer:
        """
        Update issuer record if exists, otherwise create.
        """
        issuer_did = issuer_def.get("did")
        issuer_name = issuer_def.get("name")
        issuer_abbreviation = issuer_def.get("abbreviation")
        issuer_email = issuer_def.get("email")
        issuer_url = issuer_def.get("url")
        issuer_logo = issuer_def.get("logo_b64")
        issuer_endpoint = issuer_def.get("endpoint")

        issuer, created = Issuer.objects.get_or_create(did=issuer_did)
        issuer.name = issuer_name
        issuer.abbreviation = issuer_abbreviation
        issuer.email = issuer_email
        issuer.url = issuer_url
        issuer.logo_b64 = issuer_logo
        issuer.endpoint = issuer_endpoint
        issuer.save()

        return issuer

    def update_schemas_and_ctypes(
        self, issuer, credential_type_defs
    ) -> Tuple[Sequence[Schema], Sequence[CredentialType]]:
        """
        Update schema records if they exist, otherwise create.
        Create related CredentialType records.
        """
        schemas = []
        credential_types = []

        for credential_type_def in credential_type_defs:
            # Get or create schema
            schema_name = credential_type_def.get("schema")
            schema_version = credential_type_def.get("version")
            schema_publisher_did = issuer.did

            schema, _ = Schema.objects.get_or_create(
                name=schema_name,
                version=schema_version,
                origin_did=schema_publisher_did,
            )
            schema.save()
            schemas.append(schema)

            # Get or create credential type
            credential_type_processor_config = {
                "cardinality_fields": credential_type_def.get("cardinality_fields"),
                "credential": credential_type_def.get("credential"),
                "mapping": credential_type_def.get("mapping"),
                "topic": credential_type_def.get("topic"),
            }

            credential_type, _ = CredentialType.objects.get_or_create(
                schema=schema, issuer=issuer
            )

            credential_type.description = credential_type_def.get("name")
            credential_type.processor_config = credential_type_processor_config
            credential_type.category_labels = credential_type_def.get("category_labels")
            credential_type.claim_descriptions = credential_type_def.get(
                "claim_descriptions"
            )
            credential_type.claim_labels = credential_type_def.get("claim_labels")
            credential_type.logo_b64 = credential_type_def.get("logo_b64")
            credential_type.credential_def_id = credential_type_def.get(
                "credential_def_id"
            )
            credential_type.url = credential_type_def.get("endpoint")
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

        return schemas, credential_types
