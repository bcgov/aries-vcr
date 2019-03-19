"""Credential request handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext

from ..messages.credential_request import CredentialRequest
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

        credential_offer = context.message.offer_json
        credential_request = context.message.credential_request_json

        async with context.ledger:
            schema = await context.ledger.get_schema(credential_offer["schema_id"])

        credential, credential_revocation_id = await context.issuer.create_credential(
            schema,
            credential_offer,
            credential_request,
            {"attr1": True, "attr2": 123, "test": "test"},
        )

        credential_message = Credential(
            credential_json=credential, revocation_registry_id=credential_revocation_id
        )

        await responder.send_reply(credential_message)
