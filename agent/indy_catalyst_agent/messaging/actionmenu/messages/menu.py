"""Represents an action menu."""

from typing import Sequence

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ..message_types import MENU
from ..models.menu_option import MenuOption, MenuOptionSchema

HANDLER_CLASS = (
    "indy_catalyst_agent.messaging.actionmenu.handlers.menu_handler.MenuHandler"
)


class Menu(AgentMessage):
    """Class representing an action menu."""

    class Meta:
        """Metadata for an action menu."""

        handler_class = HANDLER_CLASS
        message_type = MENU
        schema_class = "MenuSchema"

    def __init__(
        self,
        *,
        title: str = None,
        description: str = None,
        errormsg: str = None,
        options: Sequence[MenuOption] = None,
        **kwargs,
    ):
        """
        Initialize a menu object.

        Args:
            title: The menu title
            description: Introductory text for the menu
            errormsg: An optional error message to display
            options: A sequence of menu options
        """
        super(Menu, self).__init__(**kwargs)
        self.title = title
        self.description = description
        self.options = list(options) if options else []


class MenuSchema(AgentMessageSchema):
    """Menu schema class."""

    class Meta:
        """Menu schema metadata."""

        model_class = Menu

    title = fields.Str(required=False)
    description = fields.Str(required=False)
    errormsg = description = fields.Str(required=False)
    options = fields.List(fields.Nested(MenuOptionSchema), required=True)
