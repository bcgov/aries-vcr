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
    def __init__(self, host: str, port: int, message_router: Callable) -> None:
        self.host = host
        self.port = port
        self.message_router = message_router
        self.logger = logging.getLogger(__name__)

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
                    self.logger.info(msg.data)
                    await ws.close()
                    await ws.send_str("/answer")
                else:
                    self.logger.info(ws)
                    self.logger.info(msg.data)
                    await ws.send_str(msg.data + "/answer")
            elif msg.type == WSMsgType.ERROR:
                print("ws connection closed with exception %s" % ws.exception())

        print("websocket connection closed")

        return ws

        # body = await self.parse_message(request)

        # try:
        #     self.message_router(body)
        # except Exception as e:
        #     return web.Response(text=str(e), status=400)

        # return web.Response(text="OK", status=200)
