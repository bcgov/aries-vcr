import logging
from typing import Sequence

from api.v2.auth import create_issuer_user
from api.v2.models.CredentialType import CredentialType
from api.v2.models.Issuer import Issuer
from api.v2.models.Schema import Schema
from api.v2.serializers.rest import (
    CredentialTypeExtSerializer,
    IssuerSerializer,
    SchemaSerializer,
)
from agent_webhooks.utils.credential_type import CredentialTypeManager
from agent_webhooks.utils.schema import SchemaManager

LOGGER = logging.getLogger(__name__)


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

    def register_issuer(self, registration_def) -> IssuerRegistrationResult:
        """
        Perform issuer registration, updating the related database models.
        """

        credential_type_manager = CredentialTypeManager()

        issuer_registration_def = registration_def.get("issuer_registration")
        issuer_def = issuer_registration_def.get("issuer")
        credential_type_defs = issuer_registration_def.get("credential_types", [])

        # Update user and issuer
        self.update_user(issuer_def)
        issuer = self.update_issuer(issuer_def)

        # Update schemas
        schema_manager = SchemaManager()
        schemas = schema_manager.update_schemas(issuer, credential_type_defs)

        # Update credential types
        credential_types = credential_type_manager.update_credential_types(
            issuer, schemas, credential_type_defs
        )

        return IssuerRegistrationResult(issuer, schemas, credential_types)

    def update_user(self, issuer_def):
        """
        Update Django user with incoming issuer data.
        """

        issuer_did = issuer_def.get("did")
        display_name = issuer_def.get("name")
        user_email = issuer_def.get("email")

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

        issuer, _ = Issuer.objects.get_or_create(did=issuer_did)
        issuer.name = issuer_name
        issuer.abbreviation = issuer_abbreviation
        issuer.email = issuer_email
        issuer.url = issuer_url
        issuer.logo_b64 = issuer_logo
        issuer.endpoint = issuer_endpoint

        issuer.save()

        return issuer
