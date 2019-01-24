from typing import Text

from .queue.base import BaseOutboundMessageQueue


class InvalidOutboundTransportError(Exception):
    pass


class OutboundTransport:
    def __init__(self, queue: BaseOutboundMessageQueue):
        self.queue = queue

    def register_transport(self, transport_type: Text):

        # TODO: load modules dynamically
        if transport_type == "http":
            pass
        elif transport_type == "ws":
            pass
        else:
            raise InvalidOutboundTransportError()
