"""Credential request handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext

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
        credential_definition_id = credential_request["cred_def_id"]

        # TODO: This needs to retrieve by cred def id AND prover_did (to be stored on record). Then, all
        #       previous records found for that pair can be set to an invalidated state.
        #       That means that all calls to holder need to take in a connection record instead
        #       of relying on the public did.
        credential_exchange_record = await CredentialExchange.retrieve_by_tag_filter(
            context.storage,
            tag_filter={"credential_definition_id": credential_definition_id},
        )

        credential_manager = CredentialManager(context)
        await credential_manager.receive_request(credential_exchange_record, credential_request)

        # async with context.ledger:
        #     schema = await context.ledger.get_schema(credential_offer["schema_id"])
        #
        # credential, credential_revocation_id = await context.issuer.create_credential(
        #     schema,
        #     credential_offer,
        #     credential_request,
        #     {"attr1": True, "attr2": 123, "test": "test"},
        # )
        #
        # credential_message = Credential(
        #     credential_json=credential, revocation_registry_id=credential_revocation_id
        # )
        #
        # await responder.send_reply(credential_message)
