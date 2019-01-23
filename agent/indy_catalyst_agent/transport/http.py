import json
import logging
import socket
from typing import Callable

from aiohttp import web

from . import BaseTransport
from ..connections.http import HttpConnection


class HttpSetupError(Exception):
    pass


class Http(BaseTransport):
    def __init__(self, host: str, port: int, message_router: Callable) -> None:
        self.host = host
        self.port = port
        self.message_router = message_router

        self.logger = logging.getLogger(__name__)

    async def start(self) -> None:
        app = web.Application()
        app.add_routes([web.post("/", self.inbound_message_handler)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=self.host, port=self.port)
        try:
            await site.start()
        except OSError:
            raise HttpSetupError(
                f"Unable to start webserver with host '{self.host}' and port '{self.port}'\n"
            )

    async def inbound_message_handler(self, request):
        try:
            body = await request.json()
        except json.decoder.JSONDecodeError as e:
            error_message = f"Could not parse message json: {str(e)}"
            self.logger.error(error_message)
            return web.json_response(
                {"success": False, "message": error_message}, status=400
            )

        try:
            await self.message_router(
                body, HttpConnection(self.outbound_message_handler())
            )
        except Exception as e:
            error_message = f"Error handling message: {str(e)}"
            self.logger.error(error_message)
            return web.json_response(
                {"success": False, "message": error_message}, status=400
            )

        return web.Response(status=200)

    def outbound_message_handler(self):
        async def handle(message_dict: dict):
            self.logger.info(f"Sending message: {message_dict}")

        return handle

