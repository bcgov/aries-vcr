"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext

from ..messages.credential import Credential


class CredentialHandler(BaseHandler):
    """Message handler class for credential offers."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for credential offers.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"CredentialHandler called with context {context}")

        assert isinstance(context.message, Credential)

        self._logger.info(f"Received credential: {context.message.credential_json}")

        credential = context.message.credential_json

        async with context.ledger:
            credential_definition = await context.ledger.get_credential_definition(
                credential["cred_def_id"]
            )

        credential_id = await context.holder.store_credential(
            credential_definition, credential
        )
        self._logger.info("\n\n\n---")
        self._logger.info(credential_id)
