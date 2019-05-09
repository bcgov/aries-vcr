"""Represents a forwarded invitation from another agent."""

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...connections.messages.connection_invitation import (
    ConnectionInvitation,
    ConnectionInvitationSchema,
)
from ..message_types import FORWARD_INVITATION

HANDLER_CLASS = (
    "indy_catalyst_agent.messaging.introduction.handlers."
    + "forward_invitation_handler.ForwardInvitationHandler"
)


class ForwardInvitation(AgentMessage):
    """Class representing an invitation to be forwarded."""

    class Meta:
        """Metadata for a forwarded invitation."""

        handler_class = HANDLER_CLASS
        message_type = FORWARD_INVITATION
        schema_class = "ForwardInvitationSchema"

    def __init__(
        self, *, invitation: ConnectionInvitation = None, message: str = None, **kwargs
    ):
        """
        Initialize invitation object.

        Args:
            invitation: The connection invitation
            message: Comments on the introduction
        """
        super(ForwardInvitation, self).__init__(**kwargs)
        self.invitation = invitation
        self.message = message


class ForwardInvitationSchema(AgentMessageSchema):
    """ForwardInvitation request schema class."""

    class Meta:
        """ForwardInvitation request schema metadata."""

        model_class = ForwardInvitation

    invitation = fields.Nested(ConnectionInvitationSchema(), required=True)
    message = fields.Str(required=False, allow_none=True)
