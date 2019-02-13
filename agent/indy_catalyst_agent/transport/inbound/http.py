import json
import logging
import socket
from typing import Callable

from aiohttp import web

from .base import BaseInboundTransport
from ...error import BaseError
from ...wallet.util import b64_to_bytes


class HttpSetupError(BaseError):
    pass


class Transport(BaseInboundTransport):
    def __init__(self, host: str, port: int, message_router: Callable) -> None:
        self.host = host
        self.port = port
        self.message_router = message_router

        self._scheme = "http"
        self.logger = logging.getLogger(__name__)

    @property
    def scheme(self):
        return self._scheme

    async def start(self) -> None:
        app = web.Application()
        app.add_routes([web.get("/", self.invite_message_handler)])
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

    async def inbound_message_handler(self, request: web.BaseRequest):
        ctype = request.headers.get("content-type", "")
        if ctype.split(";", 1)[0].lower() == "application/json":
            body = await request.text()
        else:
            body = await request.read()
        try:
            await self.message_router(body, self._scheme)
        except Exception as e:
            error_message = f"Error handling message: {str(e)}"
            self.logger.error(error_message)
            return web.json_response(
                {"success": False, "message": error_message}, status=400
            )

        return web.Response(status=200)

    async def invite_message_handler(self, request: web.BaseRequest):
        invite = request.query.get("c_i")
        if invite:
            invite = b64_to_bytes(invite, urlsafe=True)
            await self.message_router(invite, "invitation")
            return web.Response(text="Invitation received")
        else:
            return web.Response(text="To send an invitation add ?c_i=<base64invite>")
