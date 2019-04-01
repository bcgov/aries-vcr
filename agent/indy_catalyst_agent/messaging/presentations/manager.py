"""Classes to manage presentations."""

import json
import logging
from uuid import uuid4


from ..request_context import RequestContext
from ...error import BaseError

from .models.presentation_exchange import PresentationExchange
from .messages.presentation_request import PresentationRequest


class PresentationManagerError(BaseError):
    """Presentation error."""


class PresentationManager:
    """Class for managing presentations."""

    def __init__(self, context: RequestContext):
        """
        Initialize a PresentationManager.

        Args:
            context: The context for this credential
        """
        self._context = context
        self._logger = logging.getLogger(__name__)

    @property
    def context(self) -> RequestContext:
        """
        Accessor for the current request context.

        Returns:
            The request context for this connection

        """
        return self._context

    async def create_request(
        self, requested_attributes: list, requested_predicates: list, connection_id
    ):
        """
        Create a proof request.

        """

        presentation_request = {
            "name": str(uuid4()),
            "version": str(uuid4()),
            "nonce": str(uuid4()),
            "requested_attributes": {},
            "requested_predicates": {},
        }

        for requested_attribute in requested_attributes:
            presentation_request["requested_attributes"][
                str(uuid4())
            ] = requested_attribute

        for requested_predicates in requested_predicates:
            presentation_request["requested_predicates"][
                str(uuid4())
            ] = requested_predicates

        presentation_exchange = PresentationExchange(
            connection_id=connection_id,
            initiator=PresentationExchange.INITIATOR_SELF,
            state=PresentationExchange.STATE_REQUEST_SENT,
            presentation_request=presentation_request,
        )
        await presentation_exchange.save(self.context.storage)

        presentation_request_message = PresentationRequest(
            request=json.dumps(presentation_request)
        )

        return presentation_exchange, presentation_request_message

    async def receive_request(self, proof_request: dict):
        """
        Receive a presentation request.

        Args:
            proof_request: Proof request to receive

        """
        pass
