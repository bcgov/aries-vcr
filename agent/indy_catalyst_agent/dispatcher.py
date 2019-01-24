"""
The dispatcher is responsible for coordinating data flow between handlers, providing lifecycle
hook callbacks storing state for message threads, etc.
"""

import logging

from .lifecycle import Lifecycle
from .storage.base import BaseStorage
from .messaging.agent_message import AgentMessage


class Dispatcher:
    def __init__(self, storage: BaseStorage):  # TODO: take in wallet impl as well
        self.logger = logging.getLogger(__name__)
        self.storage = storage

    async def dispatch(self, message: AgentMessage, connection):
        # TODO:
        # Create an instance of some kind of "ThreadState" or "Context"
        # using a thread id found in the message data. Messages do not
        # yet have the notion of threading
        context = {}

        # Create "connection"

        # pack/unpack

        message.handler.handle(Lifecycle, context)

        # 1. get handler result
        # 1a. Possibly communicate with service backend for instructions
        # 2. based on some logic, build a response message

        handler_response = message  # echo for now

        await connection.send_message(handler_response)

