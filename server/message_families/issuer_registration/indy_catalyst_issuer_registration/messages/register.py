"""Issuer Registration."""

from marshmallow import fields, Schema

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema

from ..message_types import REGISTER, PROTOCOL_PACKAGE


HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers"
    ".registration_handler.IssuerRegistrationHandler"
)


class IssuerRegistration(AgentMessage):
    """Class defining the structure of an issuer registration message."""

    class Meta:
        """Issuer Registration metadata class."""

        handler_class = HANDLER_CLASS
        message_type = REGISTER
        schema_class = "IssuerRegistrationSchema"

    def __init__(self, *, issuer_registration: dict, **kwargs):
        """
        Initialize issuer registration object.

        Args:
            issuer_registration: issuer metadata

        """
        super(IssuerRegistration, self).__init__(**kwargs)

        self.issuer_registration = issuer_registration


class CredentialMapping(Schema):
    """Nested mapping."""

    _from = fields.String(data_key="from", attribute="from", required=True)
    _input = fields.String(data_key="input", attribute="input", required=True)
    processor = fields.List(fields.String(), required=False)


class IssuerRegistrationSchema(AgentMessageSchema):
    """Issuer registration schema class."""

    class Meta:
        """Issuer registration schema metadata."""

        model_class = IssuerRegistration

    class IssuerRegistrationNestedSchema(Schema):
        """Issuer registration nested schema."""

        class IssuerSchema(Schema):
            """Issuer schema."""

            did = fields.Str(required=True)
            name = fields.Str(required=True)
            abbreviation = fields.Str(required=False)
            email = fields.Str(required=False)
            url = fields.Str(required=False)
            endpoint = fields.Str(required=False)
            logo_path = fields.Str(required=False, allow_none=True)
            logo_b64 = fields.Str(required=False, allow_none=True)
            labels = fields.Dict(required=False)
            abbreviations = fields.Dict(required=False)
            urls = fields.Dict(required=False)

        class CredentialType(Schema):
            """Issuer credential type schema."""

            class Credential(Schema):
                """Nested credential schema."""

                effective_date = fields.Nested(CredentialMapping(), required=True)
                inactive = fields.Nested(CredentialMapping(), required=False)
                revoked_date = fields.Nested(CredentialMapping(), required=False)

            class MappingEntry(Schema):
                """Nested mapping entry schema."""

                class Fields(Schema):
                    """Nested fields schema."""

                    _text = fields.Nested(
                        CredentialMapping(),
                        data_key="text",
                        attribute="text",
                        required=False,
                    )
                    _format = fields.Nested(
                        CredentialMapping(),
                        data_key="format",
                        attribute="format",
                        required=False,
                    )
                    _type = fields.Nested(
                        CredentialMapping(),
                        data_key="type",
                        attribute="type",
                        required=False,
                    )

                    # fields specific to an address attribute
                    _addressee = fields.Nested(
                        CredentialMapping(),
                        data_key="addressee",
                        attribute="addressee",
                        required=False,
                    )
                    _city = fields.Nested(
                        CredentialMapping(),
                        data_key="city",
                        attribute="city",
                        required=False,
                    )
                    _civic_address = fields.Nested(
                        CredentialMapping(),
                        data_key="civic_address",
                        attribute="civic_address",
                        required=False,
                    )
                    _country = fields.Nested(
                        CredentialMapping(),
                        data_key="country",
                        attribute="country",
                        required=False,
                    )
                    _postal_code = fields.Nested(
                        CredentialMapping(),
                        data_key="postal_code",
                        attribute="postal_code",
                        required=False,
                    )
                    _province = fields.Nested(
                        CredentialMapping(),
                        data_key="province",
                        attribute="province",
                        required=False,
                    )

                    value = fields.Nested(CredentialMapping(), required=False)

                _fields = fields.Nested(
                    Fields(), data_key="fields", attribute="fields", required=True
                )
                model = fields.Str(required=True)

            class Topic(Schema):
                """Nested topic schema."""

                labels = fields.Dict(required=False)

                source_id = fields.Nested(CredentialMapping(), required=False)
                _type = fields.Nested(
                    CredentialMapping(),
                    data_key="type",
                    attribute="type",
                    required=False,
                )
                name = fields.Nested(CredentialMapping(), required=False)
                related_source_id = fields.Nested(CredentialMapping(), required=False)
                related_type = fields.Nested(CredentialMapping(), required=False)
                related_name = fields.Nested(CredentialMapping(), required=False)

            cardinality_fields = fields.List(fields.String(), required=False)
            category_labels = fields.Dict(required=False)
            claim_descriptions = fields.Dict(keys=fields.Str(), values=fields.Dict(), required=False)
            claim_labels = fields.Dict(keys=fields.Str(), values=fields.Dict(), required=False)

            credential = fields.Nested(Credential(), required=False)

            name = fields.Str(required=True)
            schema = fields.Str(required=True)
            version = fields.Str(required=True)
            description = fields.Str(required=False)

            mapping = fields.List(fields.Nested(MappingEntry()), required=False)
            topic = fields.List(fields.Nested(Topic()), required=True)

            logo_b64 = fields.Str(required=False, allow_none=True)
            credential_def_id = fields.Str(required=True)
            endpoint = fields.Str(required=False)
            visible_fields = fields.List(fields.Str(), required=False)
            highlighted_attributes = fields.List(fields.Str(), required=False)
            credential_title = fields.Str(required=False)

            labels = fields.Dict(required=False)
            endpoints = fields.Dict(required=False)

        issuer = fields.Nested(IssuerSchema(), required=True)
        credential_types = fields.List(fields.Nested(CredentialType()), required=False)

    issuer_registration = fields.Nested(IssuerRegistrationNestedSchema(), required=True)
