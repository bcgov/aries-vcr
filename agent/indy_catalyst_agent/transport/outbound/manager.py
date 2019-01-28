import asyncio
import logging

from importlib import import_module
from typing import Type
from urllib.parse import urlparse

from .base import BaseOutboundTransport
from .queue.base import BaseOutboundMessageQueue
from .message import OutboundMessage
from ...classloader import ClassLoader, ModuleLoadError, ClassNotFoundError

MODULE_BASE_PATH = "indy_catalyst_agent.transport.outbound"


class OutboundTransportRegistrationError(Exception):
    pass


class OutboundTransportManager:
    def __init__(self, queue: Type[BaseOutboundMessageQueue]):
        self.logger = logging.getLogger(__name__)
        self.registered_transports = {}
        self.running_transports = {}
        self.class_loader = ClassLoader(MODULE_BASE_PATH, BaseOutboundTransport)

        self.queue = queue

    def register(self, module_path):
        # try:
        imported_class = self.class_loader.load(module_path, True)
        # except (ModuleLoadError, ClassNotFoundError):
            # raise OutboundTransportRegistrationError(f"Failed to load module {module_path}")

        try:
            schemes = imported_class.schemes
        except AttributeError:
            raise OutboundTransportRegistrationError(
                f"imported class {imported_class} does not specify a required 'schemes' attribute"
            )

        for scheme in schemes:
            # A scheme can only be registered once
            for scheme_tuple in self.registered_transports.keys():
                if scheme in scheme_tuple:
                    raise OutboundTransportRegistrationError(
                        f"cannot register transport '{module_path}' for '{scheme}' scheme"
                        + f" because the scheme has already been registered"
                    )

        self.registered_transports[schemes] = imported_class

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
            self.logger.warn(f"the uri '{uri}' does not specify a scheme")
            return

        # Look up transport that is registered to handle this scheme
        try:
            transport = next(
                transport
                for schemes, transport in self.running_transports.items()
                if scheme in schemes
            )
        except StopIteration:
            self.logger.warn(f"no transport driver exists to handle scheme '{scheme}'")
            return

        message = OutboundMessage(data=message, uri=uri)
        await transport.queue.enqueue(message)
