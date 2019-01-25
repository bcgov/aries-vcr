import asyncio
import json
import logging
import socket
from typing import Callable

from aiohttp import web, WSMsgType

from .base import BaseOutboundTransport
from .queue.base import BaseOutboundMessageQueue


class Transport(BaseOutboundTransport):
    def __init__(self, queue: BaseOutboundMessageQueue) -> None:
        self.logger = logging.getLogger(__name__)
        self.queue = queue

    async def start(self) -> None:
        async for msg in self.queue:
            self.logger.info(msg)

    def outbound_message_handler(self):
        async def handle(message_dict: dict, url: str):
            self.logger.info(f"Sending message: {message_dict}")
            async with self.client_session as session:
                async with session.post(url) as response:
                    self.logger.info(response.status)

        return handle

