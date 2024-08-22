from marshmallow import Schema, fields

from agent_webhooks.schemas import CredentialTypeDefSchema, IssuerDefSchema


class CredentialTypeRegistrationDefSchema(Schema):
    issuer = fields.Nested(IssuerDefSchema, required=True)
    credential_type = fields.Nested(
        CredentialTypeDefSchema, required=True, load_only=True
    )
    credential_types = fields.Method("get_credential_types")

    def get_credential_types(self, obj):
        return [obj.get("credential_type")]
