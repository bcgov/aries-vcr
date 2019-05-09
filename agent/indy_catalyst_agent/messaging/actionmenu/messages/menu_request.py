"""Represents a request for an action menu."""

from ...agent_message import AgentMessage, AgentMessageSchema
from ..message_types import MENU_REQUEST

HANDLER_CLASS = (
    "indy_catalyst_agent.messaging.actionmenu.handlers.menu_request_handler"
    + ".MenuRequestHandler"
)


class MenuRequest(AgentMessage):
    """Class representing a request for an action menu."""

    class Meta:
        """Metadata for action menu request."""

        handler_class = HANDLER_CLASS
        message_type = MENU_REQUEST
        schema_class = "MenuRequestSchema"

    def __init__(self, **kwargs):
        """Initialize a menu request object."""
        super(MenuRequest, self).__init__(**kwargs)


class MenuRequestSchema(AgentMessageSchema):
    """MenuRequest schema class."""

    class Meta:
        """MenuRequest schema metadata."""

        model_class = MenuRequest
