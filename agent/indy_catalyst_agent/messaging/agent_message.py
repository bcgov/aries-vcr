from abc import ABC, abstractproperty, abstractclassmethod, abstractmethod


class AgentMessage(ABC):
    @abstractproperty
    def _type(self) -> str:
        pass

    @abstractclassmethod
    def serialize(cls) -> dict:
        pass

    @abstractmethod
    def deserialize(self):
        pass
