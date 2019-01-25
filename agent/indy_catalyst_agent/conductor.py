"""
The conductor is responsible for coordinating messages that are received
over the network, communicating with the ledger, passing messages to handlers,
and storing data in the wallet.
"""

import logging

from typing import Dict

from .dispatcher import Dispatcher
from .storage.basic import BasicStorage
from .messaging.agent_message import AgentMessage
from .messaging.message_factory import MessageFactory
from .transport.inbound import InboundTransportConfiguration
from .transport.inbound.manager import InboundTransportManager
from .transport.outbound.manager import OutboundTransportManager
from .transport.outbound.queue.basic import BasicOutboundMessageQueue


class Conductor:
    def __init__(self, transport_configs: InboundTransportConfiguration) -> None:
        self.logger = logging.getLogger(__name__)
        self.transports_configs = transport_configs

    async def start(self) -> None:
        # TODO: make storage type configurable via cli params
        storage = BasicStorage()
        self.dispatcher = Dispatcher(storage)

        # Register all inbound transports
        self.inbound_transport_manager = InboundTransportManager()
        for transports_config in self.transports_configs:
            module = transports_config.module
            host = transports_config.host
            port = transports_config.port

            self.inbound_transport_manager.register(
                module, host, port, self.inbound_message_router
            )

        await self.inbound_transport_manager.start_all()

        # TODO: Set queue driver dynamically via cli args
        queue = BasicOutboundMessageQueue
        self.outbound_transport_manager = OutboundTransportManager(queue)
        self.outbound_transport_manager.register("http")
        self.outbound_transport_manager.register("ws")

        await self.outbound_transport_manager.start_all()

    async def inbound_message_router(self, message_dict: Dict) -> None:
        message = MessageFactory.make_message(message_dict)
        result = await self.dispatcher.dispatch(message, self.outbound_message_router)
        # TODO: need to use callback instead?
        #       respond immediately after message parse in case of req-res transport?
        return result.serialize()

    async def outbound_message_router(self, message: AgentMessage, connection) -> None:
        message_dict = message.serialize()
        uri = connection.endpoint
        await self.outbound_transport_manager.send_message(message_dict, uri)
