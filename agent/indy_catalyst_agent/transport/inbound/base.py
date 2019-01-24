from abc import ABC, abstractmethod
from typing import Callable


class BaseTransport(ABC):
    @abstractmethod
    def start(self, message_router: Callable) -> None:
        pass
