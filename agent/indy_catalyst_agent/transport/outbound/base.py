from abc import ABC, abstractmethod
from typing import Callable


class BaseOutboundTransport(ABC):
    @abstractmethod
    def start(self) -> None:
        pass
