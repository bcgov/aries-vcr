import logging
from importlib import import_module

TRANSPORT_BASE_PATH = "indy_catalyst_agent.transport.inbound"


class InboundTransportManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.transports = []

    def register(self, module_path, host, port, message_handler):
        relative_transport_path = ".".join([TRANSPORT_BASE_PATH, module_path])
        try:
            # First we try importing any built-in inbound transports by name
            imported_transport_module = import_module(relative_transport_path)
        except ModuleNotFoundError:
            try:
                # Then we try importing transports available in external modules
                imported_transport_module = import_module(module_path)
            except ModuleNotFoundError:
                self.logger.warning(
                    "Unable to import inbound transport module {}. "
                    + f"Module paths attempted: {relative_transport_path}, {module_path}"
                )
                return

        self.transports.append(
            imported_transport_module.Transport(host, port, message_handler)
        )

    async def start_all(self):
        for transport in self.transports:
            await transport.start()
