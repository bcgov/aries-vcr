import asyncio
import json
import logging
import socket
from typing import Callable

from . import BaseTransport

from aiohttp import web, WSMsgType


class InvalidMessageError(Exception):
    pass


class WsSetupError(Exception):
    pass


class Ws(BaseTransport):
    def __init__(self, host: str, port: int, message_callback: Callable) -> None:
        self.host = host
        self.port = port
        self.message_callback = message_callback

        self.logger = logging.getLogger(__name__)
        self.message_queue = asyncio.Queue()

    async def start(self) -> None:
        app = web.Application()
        app.add_routes([web.get("/", self.message_handler)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=self.host, port=self.port)
        try:
            await site.start()
        except OSError:
            raise WsSetupError(
                f"Unable to start webserver with host '{self.host}' and port '{self.port}'\n"
            )

    async def parse_message(self, request):
        try:
            body = await request.json()
        except json.JSONDecodeError:
            raise InvalidMessageError(
                "Request body must contain a valid application/json payload"
            )
        return body

    async def message_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "close":
                    await ws.close()
                else:
                    try:
                        message_dict = json.loads(msg.data)
                    except json.decoder.JSONDecodeError as e:
                        self.logger.error(f"Could not parse message json: {str(e)}")
                        await ws.send_json({"success": False, "message": str(e)})
                        continue

                    try:
                        from ..connections.websocket import WebsocketConnection

                        await self.message_callback(
                            message_dict, WebsocketConnection(ws.send_json)
                        )

                    except Exception as e:
                        self.logger.error(f"Error handling message: {str(e)}")
                        await ws.send_json({"success": False, "message": str(e)})
                        continue

            elif msg.type == WSMsgType.ERROR:
                self.logger.error(
                    "ws connection closed with exception %s" % ws.exception()
                )

        self.logger.info("websocket connection closed")
        return ws

