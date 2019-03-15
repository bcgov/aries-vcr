"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext

from ..messages.credential_offer import CredentialOffer
from ..messages.credential_request import CredentialRequest


class CredentialOfferHandler(BaseHandler):
    """Message handler class for credential offers."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for credential offers.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"CredentialOfferHandler called with context {context}")

        assert isinstance(context.message, CredentialOffer)

        self._logger.info("Received credential offer: %s", context.message.offer_json)

        # TODO: update credential state
        # TODO: don't autorespond by default

        credential_offer = context.message.offer_json

        async with context.ledger:
            credential_definition = await context.ledger.get_credential_definition(
                credential_offer["cred_def_id"]
            )

        credential_request = await context.holder.create_credential_request(
            credential_offer, credential_definition
        )

        credential_request = CredentialRequest(
            offer_json=credential_offer, credential_request_json=credential_request
        )

        await responder.send_reply(credential_request)
