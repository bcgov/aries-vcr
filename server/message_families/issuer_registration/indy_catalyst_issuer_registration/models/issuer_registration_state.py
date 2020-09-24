"""Handle issuer registration information with non-secrets storage."""


from marshmallow import fields

from aries_cloudagent.messaging.models.base_record import BaseRecord, BaseRecordSchema


class IssuerRegistrationState(BaseRecord):
    """Represents a issuer registration."""

    class Meta:
        """IssuerRegistrationState metadata."""

        schema_class = "IssuerRegistrationStateSchema"

    RECORD_TYPE = "issuer_registration"
    TAG_NAMES = {"connection_id", "~thread_id", "initiator", "state"}
    WEBHOOK_TOPIC = "issuer_registration"

    INITIATOR_SELF = "self"
    INITIATOR_EXTERNAL = "external"

    STATE_REGISTRATION_SENT = "registration_sent"
    STATE_REGISTRATION_RECEIVED = "registration_received"

    def __init__(
        self,
        *,
        issuer_registration_id: str = None,
        connection_id: str = None,
        issuer_registration: dict = None,
        thread_id: str = None,
        initiator: str = None,
        state: str = None,
        error_msg: str = None,
        **kwargs
    ):
        """Initialize a new IssuerRegistrationState."""
        super().__init__(
            issuer_registration_id, state or self.STATE_REGISTRATION_SENT, **kwargs
        )
        self.connection_id = connection_id
        self.issuer_registration = issuer_registration
        self.thread_id = thread_id
        self.initiator = initiator
        self.state = state
        self.error_msg = error_msg

    @property
    def issuer_registration_id(self) -> str:
        """Accessor for the ID associated with this exchange."""
        return self._id

    @property
    def record_value(self) -> dict:
        """Accessor to for the JSON record value properties for this connection."""
        return {
            prop: getattr(self, prop) for prop in ("issuer_registration", "error_msg",)
        }


class IssuerRegistrationStateSchema(BaseRecordSchema):
    """Schema to allow serialization/deserialization of issuer registration records."""

    class Meta:
        """IssuerRegistrationStateSchema metadata."""

        model_class = IssuerRegistrationState

    issuer_registration_id = fields.Str(required=False)
    connection_id = fields.Str(required=False)
    issuer_registration = fields.Dict(required=False)
    thread_id = fields.Str(required=False)
    initiator = fields.Str(required=False)
    state = fields.Str(required=False)
    error_msg = fields.Str(required=False)
