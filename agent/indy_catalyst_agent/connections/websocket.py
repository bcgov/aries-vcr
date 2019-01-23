from typing import Coroutine

from .base import BaseConnection

from ..messaging.agent_message import AgentMessage


class WebsocketConnection(BaseConnection):
    def __init__(self, send: Coroutine):
        self.send = send

    async def send_message(self, message: AgentMessage):
        """
        Send a message to this connection
        """
        message_dict = message.serialize()
        await self.send(message_dict)
