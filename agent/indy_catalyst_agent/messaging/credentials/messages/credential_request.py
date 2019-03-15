"""A credential request content message."""

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...message_types import MessageTypes

HANDLER_CLASS = (
    "indy_catalyst_agent.messaging.credentials.handlers."
    + "credential_request_handler.CredentialRequestHandler"
)


class CredentialRequest(AgentMessage):
    """Class representing a credential request."""

    class Meta:
        """CredentialRequest metadata."""

        handler_class = HANDLER_CLASS
        schema_class = "CredentialRequestSchema"
        message_type = MessageTypes.CREDENTIAL_REQUEST.value

    def __init__(
        self, *, offer_json: dict = None, credential_request_json: dict = None, **kwargs
    ):
        """
        Initialize credential request object.

        Args:
            offer_json: Credential offer json string
            credential_request_json: Credential request json string
            
        """
        super(CredentialRequest, self).__init__(**kwargs)
        self.offer_json = offer_json
        self.credential_request_json = credential_request_json


class CredentialRequestSchema(AgentMessageSchema):
    """Credential request schema."""

    class Meta:
        """Credential request schema metadata."""

        model_class = CredentialRequest

    offer_json = fields.Dict(required=True)
    credential_request_json = fields.Dict(required=True)
