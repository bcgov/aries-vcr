"""Credential request handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext

from ...connections.models.connection_record import ConnectionRecord

from ..manager import CredentialManager
from ..messages.credential_request import CredentialRequest
from ..models.credential_exchange import CredentialExchange
from ..messages.credential import Credential


class CredentialRequestHandler(BaseHandler):
    """Message handler class for credential requests."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for credential requests.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"CredentialRequestHandler called with context {context}")

        assert isinstance(context.message, CredentialRequest)

        self._logger.info(
            "Received credential request: %s", context.message.serialize(as_string=True)
        )

        credential_request = context.message.credential_request_json

        credential_manager = CredentialManager(context)
        await credential_manager.receive_request(
            credential_request
        )
