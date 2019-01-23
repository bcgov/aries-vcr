
from abc import ABC, abstractmethod
from typing import Mapping, Sequence

from ..messaging.agent_message import AgentMessage


class BaseConnection(ABC):
    """
    Abstract connection interface
    """

    @abstractmethod
    async def send_message(self, message: AgentMessage):
        """
        Send a message to this connection
        """
        pass
