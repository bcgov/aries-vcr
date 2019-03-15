"""A credential offer content message."""

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...message_types import MessageTypes


HANDLER_CLASS = (
    "indy_catalyst_agent.messaging.credentials.handlers."
    + "credential_offer_handler.CredentialOfferHandler"
)


class CredentialOffer(AgentMessage):
    """Class representing a credential offer."""

    class Meta:
        """CredentialOffer metadata."""

        handler_class = HANDLER_CLASS
        schema_class = "CredentialOfferSchema"
        message_type = MessageTypes.CREDENTIAL_OFFER.value

    def __init__(self, *, offer_json: dict = None, **kwargs):
        """
        Initialize credential offer object.

        Args:
            offer_json: Credential offer json
        """
        super(CredentialOffer, self).__init__(**kwargs)
        self.offer_json = offer_json


class CredentialOfferSchema(AgentMessageSchema):
    """Credential offer schema."""

    class Meta:
        """Credential offer schema metadata."""

        model_class = CredentialOffer

    offer_json = fields.Dict(required=True)
