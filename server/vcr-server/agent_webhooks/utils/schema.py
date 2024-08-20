import logging
from typing import Sequence, Tuple

from api.v2.models.Schema import Schema

LOGGER = logging.getLogger(__name__)


class SchemaManager:
    """
    Manage the creation and updating of Schema records.
    """

    def update_schemas(self, issuer, credential_type_defs) -> Sequence[Schema]:
        """
        Update schema records if they exist, otherwise create.
        """

        schemas = []

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

        return schemas
