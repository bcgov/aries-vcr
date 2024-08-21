from marshmallow import Schema, fields


class IssuerDefSchema(Schema):
    name = fields.String(required=True)
    did = fields.String(required=True)
    abbreviation = fields.String(required=True)
    email = fields.String(required=True)
    url = fields.String(required=True)
    endpoint = fields.String()
    logo_b64 = fields.String()
