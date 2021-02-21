"""Issuer registration handler."""

from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)
from ..messages.register import IssuerRegistration
from ..manager import IssuerRegistrationManager


class IssuerRegistrationHandler(BaseHandler):
    """Message handler class for issuer registration."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for issuer registration.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"IssuerRegistrationHandler called with context {context}")
        assert isinstance(context.message, IssuerRegistration)
        session = await context.session()

        self._logger.info("Received issuer registration: %s", context.message)

        issuer_registration_manager = IssuerRegistrationManager(session)

        await issuer_registration_manager.receive_registration(
            context.connection_record.connection_id, context.message
        )
