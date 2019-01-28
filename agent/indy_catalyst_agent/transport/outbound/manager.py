import asyncio
import logging

from importlib import import_module
from typing import Type
from urllib.parse import urlparse

from .queue.base import BaseOutboundMessageQueue
from .message import OutboundMessage

MODULE_BASE_PATH = "indy_catalyst_agent.transport.outbound"


class OutboundTransportManagerError(Exception):
    pass


class OutboundTransportManager:
    def __init__(self, queue: Type[BaseOutboundMessageQueue]):
        self.logger = logging.getLogger(__name__)
        self.registered_transports = {}
        self.running_transports = {}

        self.queue = queue

    def register(self, module_path):
        # TODO: move this dynamic import stuff to a shared module
        relative_transport_path = ".".join([MODULE_BASE_PATH, module_path])
        try:
            # First we try importing any built-in inbound transports by name
            imported_transport_module = import_module(relative_transport_path)
        except ModuleNotFoundError:
            try:
                # Then we try importing transports available in external modules
                imported_transport_module = import_module(module_path)
            except ModuleNotFoundError:
                self.logger.warning(
                    "Unable to import outbound transport module {}. "
                    + f"Module paths attempted: {relative_transport_path}, {module_path}"
                )
                return

        # TODO: find class based on inheritance of trusted base class instead of
        #       looking for "Transport" attribute?
        try:
            schemes = imported_transport_module.SCHEMES
            transport_class = imported_transport_module.Transport
        except AttributeError:
            self.logger.error(f"OutboundTransports must define SCHEMES and Transport.")
            return

        for scheme in schemes:
            # A scheme can only be registered once
            if scheme in self.registered_transports:
                raise OutboundTransportManagerError(
                    f"Cannot register transport '{module_path}' for '{scheme}' scheme"
                    + f" because the scheme has already been registered."
                )

        self.registered_transports[schemes] = transport_class

    async def start(self, schemes, transport):
        # All transports use the same queue implementation
        async with transport(self.queue()) as t:
            self.running_transports[schemes] = t
            await t.start()

    async def start_all(self):
        for schemes, transport_class in self.registered_transports.items():
            asyncio.create_task(self.start(schemes, transport_class))

    async def send_message(self, message, uri):
        # Grab the scheme from the uri
        scheme = urlparse(uri).scheme
        if scheme == "":
            self.logger.warn(f"The uri '{uri}' does not specify a scheme")
            return

        # Look up transport that is registered to handle this scheme
        try:
            transport = next(
                transport
                for schemes, transport in self.running_transports.items()
                if scheme in schemes
            )
        except StopIteration:
            self.logger.warn(f"No transport driver exists to handle scheme '{scheme}'")
            return

        message = OutboundMessage(data=message, uri=uri)
        await transport.queue.enqueue(message)
