from collections import namedtuple

from abc import ABC, abstractmethod
from typing import Callable

InboundTransportConfiguration = namedtuple(
    "InboundTransportConfiguration", "module host port"
)


class InvalidTransportError(Exception):
    pass


class BaseTransport(ABC):
    @abstractmethod
    def start(self, message_router: Callable) -> None:
        pass
