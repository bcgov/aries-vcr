"""Outbound transport manager."""

import asyncio
import logging

from typing import Type
from urllib.parse import urlparse

from .base import BaseOutboundTransport
from ...classloader import ClassLoader
from ...error import BaseError
from .queue.base import BaseOutboundMessageQueue
from .message import OutboundMessage


MODULE_BASE_PATH = "indy_catalyst_agent.transport.outbound"


class OutboundTransportRegistrationError(BaseError):
    """Outbound transport registration error."""

    pass


class OutboundTransportManager:
    """Outbound transport manager class."""

    def __init__(self, queue: Type[BaseOutboundMessageQueue]):
        """
        Initialize a `OutboundTransportManager` instance.

        Args:
            queue: `BaseOutboundMessageQueue` implementation to use

        """
        self.logger = logging.getLogger(__name__)
        self.registered_transports = {}
        self.running_transports = {}
        self.class_loader = ClassLoader(MODULE_BASE_PATH, BaseOutboundTransport)
        self.queue = queue

    def register(self, module_path):
        """
        Register a new outbound transport.

        Args:
            module_path: Module path to register

        Raises:
            OutboundTransportRegistrationError: If the imported class does not
                specify a schemes attribute
            OutboundTransportRegistrationError: If the scheme has already been
                registered

        """
        imported_class = self.class_loader.load(module_path, True)

        try:
            schemes = imported_class.schemes
        except AttributeError:
            raise OutboundTransportRegistrationError(
                f"Imported class {imported_class} does not "
                + "specify a required 'schemes' attribute"
            )

        for scheme in schemes:
            # A scheme can only be registered once
            for scheme_tuple in self.registered_transports.keys():
                if scheme in scheme_tuple:
                    raise OutboundTransportRegistrationError(
                        f"Cannot register transport '{module_path}'"
                        + f"for '{scheme}' scheme because the scheme"
                        + "has already been registered"
                    )

        self.registered_transports[schemes] = imported_class

    async def start(self, schemes, transport):
        """Start the transport."""
        # All transports share the same queue
        async with transport(self.queue()) as t:
            self.running_transports[schemes] = t
            await t.start()

    async def start_all(self):
        """Start all transports."""
        for schemes, transport_class in self.registered_transports.items():
            # Don't block the loop
            # asyncio.create_task(self.start(schemes, transport_class))
            asyncio.ensure_future(self.start(schemes, transport_class))

    async def send_message(self, message, uri: str):
        """
        Send a message.

        Find a registered transport for the scheme in the uri and
        use it to send the message.

        Args:
            message: The agent message to send
            uri: Where are you sending the message

        """
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
