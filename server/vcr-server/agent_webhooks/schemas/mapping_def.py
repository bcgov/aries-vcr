from marshmallow import fields

from agent_webhooks.enums import MappingTypeEnum
from agent_webhooks.schemas import PathBaseSchema

class MappingDefSchema(PathBaseSchema):

    type = fields.Enum(MappingTypeEnum, by_value=True, required=True)
    name = fields.String(required=True)