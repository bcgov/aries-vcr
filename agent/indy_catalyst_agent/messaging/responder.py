"""
A message responder.

The responder is provided to message handlers to enable them to send a new message
in response to the message being handled.
"""

from abc import ABC, abstractmethod
from typing import Union

from ..error import BaseError

from .agent_message import AgentMessage
from .connections.models.connection_target import ConnectionTarget
from .outbound_message import OutboundMessage


class ResponderError(BaseError):
    """Responder error."""


class BaseResponder(ABC):
    """Interface for message handlers to send responses."""

    def __init__(
        self,
        *,
        connection_id: str = None,
        reply_socket_id: str = None,
        reply_to_verkey: str = None,
        target: ConnectionTarget = None,
    ):
        """Initialize a base responder."""
        self.connection_id = connection_id
        self.reply_socket_id = reply_socket_id
        self.reply_to_verkey = reply_to_verkey
        self.target = target

    async def create_outbound(
        self,
        message: Union[AgentMessage, str, bytes],
        *,
        connection_id: str = None,
        reply_socket_id: str = None,
        reply_thread_id: str = None,
        reply_to_verkey: str = None,
        target: ConnectionTarget = None,
    ) -> OutboundMessage:
        """Create an OutboundMessage from a message payload."""
        if isinstance(message, AgentMessage):
            payload = message.to_json()
            encoded = False
            if not reply_thread_id:
                reply_thread_id = message._thread_id
        else:
            payload = message
            encoded = True
        return OutboundMessage(
            payload,
            connection_id=connection_id,
            encoded=encoded,
            reply_socket_id=reply_socket_id,
            reply_thread_id=reply_thread_id,
            reply_to_verkey=reply_to_verkey,
            target=target,
        )

    async def send(self, message: Union[AgentMessage, str, bytes], **kwargs):
        """Convert a message to an OutboundMessage and send it."""
        outbound = await self.create_outbound(message, **kwargs)
        await self.send_outbound(outbound)

    async def send_reply(self, message: Union[AgentMessage, str, bytes]):
        """
        Send a reply to an incoming message.

        Args:
            message: the `AgentMessage`, or pre-packed str or bytes to reply with

        Raises:
            ResponderError: If there is no active connection

        """
        outbound = await self.create_outbound(
            message,
            connection_id=self.connection_id,
            reply_socket_id=self.reply_socket_id,
            reply_to_verkey=self.reply_to_verkey,
            target=self.target,
        )
        await self.send_outbound(outbound)

    @abstractmethod
    async def send_outbound(self, message: OutboundMessage):
        """
        Send an outbound message.

        Args:
            message: The `OutboundMessage` to be sent
        """


class MockResponder(BaseResponder):
    """Mock responder implementation for use by tests."""

    def __init__(self):
        """Initialize the mock responder."""
        self.messages = []

    async def send(self, message: Union[AgentMessage, str, bytes], **kwargs):
        """Convert a message to an OutboundMessage and send it."""
        self.messages.append((message, kwargs))

    async def send_reply(self, message: Union[AgentMessage, str, bytes]):
        """Send a reply to an incoming message."""
        self.messages.append((message, None))

    async def send_outbound(self, message: OutboundMessage):
        """Send an outbound message."""
        self.messages.append((message, None))
