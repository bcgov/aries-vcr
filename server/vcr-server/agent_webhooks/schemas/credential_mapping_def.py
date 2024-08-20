from marshmallow import fields

from agent_webhooks.schemas import PathBaseSchema


class CredentialMappingDefSchema(PathBaseSchema):
    name = fields.String(required=True)
