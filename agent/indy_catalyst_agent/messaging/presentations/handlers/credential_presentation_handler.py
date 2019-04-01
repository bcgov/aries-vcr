"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext

from ..manager import PresentationManager
from ..messages.credential_presentation import CredentialPresentation


class CredentialPresentationHandler(BaseHandler):
    """Message handler class for credential presentations."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for credential presentations.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(
            f"CredentialPresentationHandler called with context {context}"
        )
        assert isinstance(context.message, CredentialPresentation)
        self._logger.info(
            f"Received credential presentation: {context.message.presentation}"
        )
