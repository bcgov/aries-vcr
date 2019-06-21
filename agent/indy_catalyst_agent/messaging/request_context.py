"""
Request context class.

A request context provides everything required by handlers and other parts
of the system to process a message.
"""

from typing import Mapping

from ..config.injection_context import InjectionContext

from .agent_message import AgentMessage
from .connections.models.connection_record import ConnectionRecord
from .message_delivery import MessageDelivery


class RequestContext(InjectionContext):
    """Context established by the Conductor and passed into message handlers."""

    def __init__(self, *, settings: Mapping[str, object] = None):
        """Initialize an instance of RequestContext."""
        super().__init__(settings=settings)
        self._connection_active = False
        self._connection_record = None
        self._message = None
        self._message_delivery = None

    @property
    def connection_active(self) -> bool:
        """
        Accessor for the flag indicating an active connection with the sender.

        Returns:
            True if the connection is active, else False

        """
        return self._connection_active

    @connection_active.setter
    def connection_active(self, active: bool):
        """
        Setter for the flag indicating an active connection with the sender.

        Args:
            active: The new active value

        """
        self._connection_active = active

    @property
    def connection_record(self) -> ConnectionRecord:
        """Accessor for the related connection record."""
        return self._connection_record

    @connection_record.setter
    def connection_record(self, record: ConnectionRecord):
        """Setter for the related connection record.

        :param record: ConnectionRecord:

        """
        self._connection_record = record

    @property
    def default_endpoint(self) -> str:
        """
        Accessor for the default agent endpoint (from agent config).

        Returns:
            The default agent endpoint

        """
        return self.settings["default_endpoint"]

    @default_endpoint.setter
    def default_endpoint(self, endpoint: str):
        """
        Setter for the default agent endpoint (from agent config).

        Args:
            endpoint: The new default endpoint

        """
        self.settings["default_endpoint"] = endpoint

    @property
    def default_label(self) -> str:
        """
        Accessor for the default agent label (from agent config).

        Returns:
            The default label

        """
        return self.settings["default_label"]

    @default_label.setter
    def default_label(self, label: str):
        """
        Setter for the default agent label (from agent config).

        Args:
            label: The new default label

        """
        self.settings["default_label"] = label

    @property
    def message(self) -> AgentMessage:
        """
        Accessor for the deserialized message instance.

        Returns:
            This context's agent message

        """
        return self._message

    @message.setter
    def message(self, msg: AgentMessage):
        """
        Setter for the deserialized message instance.

        Args:
            msg: This context's new agent message
        """
        self._message = msg

    @property
    def message_delivery(self) -> MessageDelivery:
        """
        Accessor for the message delivery information.

        Returns:
            This context's message delivery information

        """
        return self._message_delivery

    @message_delivery.setter
    def message_delivery(self, delivery: MessageDelivery):
        """
        Setter for the message delivery information.

        Args:
            msg: This context's new message delivery information
        """
        self._message_delivery = delivery

    def __repr__(self) -> str:
        """
        Provide a human readable representation of this object.

        Returns:
            A human readable representation of this object

        """
        skip = ()
        items = (
            "{}={}".format(k, repr(v))
            for k, v in self.__dict__.items()
            if k not in skip
        )
        return "<{}({})>".format(self.__class__.__name__, ", ".join(items))

    def copy(self) -> "RequestContext":
        """Produce a copy of the request context instance."""
        return super().copy()
