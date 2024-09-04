from marshmallow import fields

from agent_webhooks.schemas import CredentialTypeDefSchema, IssuerRegistrationDefSchema


class CredentialTypeRegistrationDefSchema(IssuerRegistrationDefSchema):
    credential_type = fields.Nested(
        CredentialTypeDefSchema, required=True, load_only=True
    )

    def get_issuer_registration(self, obj):
        return {
            "issuer": obj.get("issuer"),
            "credential_types": [obj.get("credential_type")],
        }
