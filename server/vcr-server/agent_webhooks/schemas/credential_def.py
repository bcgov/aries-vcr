from marshmallow import Schema, fields

from agent_webhooks.enums import FormatEnum


class CredentialDefSchema(Schema):
    format = fields.Enum(FormatEnum, by_value=True, required=True)
    schema = fields.String(required=True)
    version = fields.String(required=True)
    origin_did = fields.String(required=True)
    credential_id = fields.String(required=True)
    # We don't make any assumptions about the fields in the raw_data dictionary
    # since there are different credential formats. Eventually we should define
    # schemas for different credential formats.
    raw_data = fields.Dict(required=True)
