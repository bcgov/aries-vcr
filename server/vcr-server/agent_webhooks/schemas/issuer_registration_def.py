from marshmallow import Schema, fields

from agent_webhooks.schemas import IssuerDefSchema


class IssuerRegistrationDefSchema(Schema):
    issuer = fields.Nested(IssuerDefSchema, required=True, load_only=True)
    issuer_registration = fields.Method("get_issuer_registration")

    def get_issuer_registration(self, obj):
        return {"issuer": obj.get("issuer")}
