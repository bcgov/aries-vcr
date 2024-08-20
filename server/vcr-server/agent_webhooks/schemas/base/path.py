from marshmallow import Schema, fields


class PathBaseSchema(Schema):

    path = fields.String(required=True)