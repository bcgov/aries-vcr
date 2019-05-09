"""Represents an request for an invitation from the introduction service."""

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ..message_types import INVITATION_REQUEST

HANDLER_CLASS = (
    "indy_catalyst_agent.messaging.introduction.handlers."
    + "invitation_request_handler.InvitationRequestHandler"
)


class InvitationRequest(AgentMessage):
    """Class representing an invitation request."""

    class Meta:
        """Metadata for an invitation request."""

        handler_class = HANDLER_CLASS
        message_type = INVITATION_REQUEST
        schema_class = "InvitationRequestSchema"

    def __init__(self, *, responder: str = None, message: str = None, **kwargs):
        """
        Initialize invitation request object.

        Args:
            responder: The name of the agent initiating the introduction
            message: Comments on the introduction
        """
        super(InvitationRequest, self).__init__(**kwargs)
        self.responder = responder
        self.message = message


class InvitationRequestSchema(AgentMessageSchema):
    """Invitation request schema class."""

    class Meta:
        """Invitation request schema metadata."""

        model_class = InvitationRequest

    responder = fields.Str(required=True)
    message = fields.Str(required=False, allow_none=True)
