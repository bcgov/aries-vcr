"""
The conductor is responsible for coordinating messages that are received
over the network, communicating with the ledger, passing messages to handlers,
and storing data in the wallet.
"""

from importlib import import_module
import logging

from .dispatcher import Dispatcher

from .storage.basic import BasicStorage

from .messaging.message_factory import MessageFactory

TRANSPORT_BASE_PATH = "indy_catalyst_agent.transport"


class Conductor:
    def __init__(self, parsed_transports: list) -> None:
        self.logger = logging.getLogger(__name__)
        self.transports = parsed_transports

    async def start(self) -> None:
        # TODO: make storage type configurable via cli params
        storage = BasicStorage()
        self.dispatcher = Dispatcher(storage)

        for transport in self.transports:
            transport_module = transport["transport"]
            inbound_transport_path = ".".join(
                [TRANSPORT_BASE_PATH, "inbound", transport_module]
            )
            try:
                # First we try importing any built-in inbound transports by name
                imported_transport_module = import_module(inbound_transport_path)
            except ModuleNotFoundError:
                try:
                    # Then we try importing transports available in external modules
                    imported_transport_module = import_module(transport_module)
                except ModuleNotFoundError:
                    self.logger.warning(
                        "Unable to import inbound transport module {}. "
                        + f"Module paths attempted: {inbound_transport_path}, {transport_module}"
                    )
                    continue

            transport_instance = imported_transport_module.Transport(
                transport["host"], transport["port"], self.message_router
            )

            await transport_instance.start()

    async def message_router(self, message_dict: dict, connection) -> None:
        message = MessageFactory.make_message(message_dict)
        await self.dispatcher.dispatch(message, connection)
