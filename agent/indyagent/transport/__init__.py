from abc import ABC, abstractmethod
from typing import Callable


class InvalidTransportException(Exception):
    pass


class Transport(ABC):
    @abstractmethod
    def setup(self, message_router: Callable) -> None:
        pass
