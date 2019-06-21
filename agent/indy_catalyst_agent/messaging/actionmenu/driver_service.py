"""Driver-based action menu service classes."""

import asyncio
import logging

from ..agent_message import AgentMessage
from ..connections.models.connection_record import ConnectionRecord
from ..util import send_webhook

from .base_service import BaseMenuService
from .messages.menu import Menu

LOGGER = logging.getLogger(__name__)


class DriverMenuService(BaseMenuService):
    """Driver-based action menu service."""

    async def get_active_menu(
        self, connection: ConnectionRecord = None, thread_id: str = None
    ) -> Menu:
        """
        Render the current menu.

        Args:
            connection: The active connection record
            thread_id: The thread identifier from the requesting message.
        """
        asyncio.ensure_future(
            send_webhook(
                "get-active-menu",
                {
                    "connection_id": connection and connection.connection_id,
                    "thread_id": thread_id,
                },
            )
        )
        return None

    async def perform_menu_action(
        self,
        action_name: str,
        action_params: dict,
        connection: ConnectionRecord = None,
        thread_id: str = None,
    ) -> AgentMessage:
        """
        Perform an action defined by the active menu.

        Args:
            action_name: The unique name of the action being performed
            action_params: A collection of parameters for the action
            connection: The active connection record
            thread_id: The thread identifier from the requesting message.
        """
        asyncio.ensure_future(
            send_webhook(
                "perform-menu-action",
                {
                    "connection_id": connection and connection.connection_id,
                    "thread_id": thread_id,
                    "action_name": action_name,
                    "action_params": action_params,
                },
            )
        )
        return None
