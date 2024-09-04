from marshmallow import Schema, fields

from agent_webhooks.schemas import PathBaseSchema as PathSchema

class TopicDefSchema(Schema):

    type = fields.String(required=True)
    source_id = fields.Nested(PathSchema, required=True)