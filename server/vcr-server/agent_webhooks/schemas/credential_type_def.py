from marshmallow import Schema, fields

from agent_webhooks.enums import FormatEnum, MappingTypeEnum
from agent_webhooks.schemas import (
    CredentialMappingDefSchema,
    MappingDefSchema,
    TopicDefSchema,
)


class CredentialTypeDefSchema(Schema):
    format = fields.Enum(FormatEnum, by_value=True, required=True)
    schema = fields.String(required=True)
    version = fields.String(required=True)
    origin_did = fields.String(required=True)
    topic = fields.Nested(TopicDefSchema, required=True)
    mappings = fields.List(fields.Nested(MappingDefSchema))
    credential = fields.Dict(
        keys=fields.Enum(MappingTypeEnum, by_value=True),
        values=fields.Nested(CredentialMappingDefSchema),
    )
