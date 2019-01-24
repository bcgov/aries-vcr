"""
The conductor is responsible for coordinating messages that are received
over the network, communicating with the ledger, passing messages to handlers,
and storing data in the wallet.
"""

import logging

from typing import Dict

from .dispatcher import Dispatcher
from .storage.basic import BasicStorage
from .messaging.message_factory import MessageFactory
from .transport.inbound import InboundTransportConfiguration
from .transport.inbound.manager import InboundTransportManager


class Conductor:
    def __init__(self, transport_configs: InboundTransportConfiguration) -> None:
        self.logger = logging.getLogger(__name__)
        self.transports_configs = transport_configs
        self.inbound_transport_manager = InboundTransportManager()

    async def start(self) -> None:
        # TODO: make storage type configurable via cli params
        storage = BasicStorage()
        self.dispatcher = Dispatcher(storage)

        # Register all inbound transports
        for transports_config in self.transports_configs:
            module = transports_config.module
            host = transports_config.host
            port = transports_config.port

            self.inbound_transport_manager.register(
                module, host, port, self.message_handler
            )

        await self.inbound_transport_manager.start_all()

    async def message_handler(self, message_dict: Dict) -> None:
        message = MessageFactory.make_message(message_dict)
        await self.dispatcher.dispatch(message)

