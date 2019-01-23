"""
The conductor is responsible for coordinating messages that are received
over the network, communicating with the ledger, passing messages to handlers,
and storing data in the wallet.
"""

import logging

from .dispatcher import Dispatcher

from .transport.http import Http as HttpTransport
from .transport.ws import Ws as WsTransport
from .transport import InvalidTransportError, VALID_TRANSPORTS

from .storage.basic import BasicStorage

from .messaging.message_factory import MessageFactory


class Conductor:
    def __init__(self, parsed_transports: list) -> None:
        self.logger = logging.getLogger(__name__)
        self.transports = parsed_transports

    async def start(self) -> None:
        # TODO: make storage type configurable via cli params
        storage = BasicStorage()
        self.dispatcher = Dispatcher(storage)

        for transport in self.transports:
            if transport["transport"] == "http":
                transport = HttpTransport(
                    transport["host"], transport["port"], self.transport_callback
                )
                await transport.start()
            elif transport["transport"] == "ws":
                transport = WsTransport(
                    transport["host"], transport["port"], self.transport_callback
                )
                await transport.start()
            else:
                # TODO: make this pluggable
                raise InvalidTransportError("Available transports: http")

    async def transport_callback(self, message_dict: dict, connection) -> None:
        message = MessageFactory.make_message(message_dict)
        await self.dispatcher.dispatch(message, connection)
