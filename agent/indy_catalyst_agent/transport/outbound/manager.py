import logging
from importlib import import_module

from .queue.base import BaseOutboundMessageQueue

MODULE_BASE_PATH = "indy_catalyst_agent.transport.outbound"


class OutboundTransportManager:
    def __init__(self, queue: BaseOutboundMessageQueue):
        self.logger = logging.getLogger(__name__)
        self.transports = []

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
        #       looking for "Transport" attribute
        self.transports.append(imported_transport_module.Transport(self.queue))

    async def start_all(self):
        for transport in self.transports:
            await transport.start()

    async def send_message(self, message):
        await self.queue.enqueue(message)
