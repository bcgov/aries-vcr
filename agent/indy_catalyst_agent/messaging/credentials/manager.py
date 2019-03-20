"""Classes to manage credentials."""

import json
import logging

from ..request_context import RequestContext
from ...error import BaseError

from .messages.credential_request import CredentialRequest
from .messages.credential_offer import CredentialOffer
from .models.credential_exchange import CredentialExchange


class CredentialManagerError(BaseError):
    """Credential error."""


class CredentialManager:
    """Class for managing credentials."""

    def __init__(self, context: RequestContext):
        """
        Initialize a CredentialManager.

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

    async def create_offer(self, credential_definition_id, connection_id):

        credential_offer = await self.context.issuer.create_credential_offer(
            credential_definition_id
        )
        credential_exchange = CredentialExchange(
            connection_id=connection_id,
            initiator=CredentialExchange.INITIATOR_SELF,
            state=CredentialExchange.STATE_OFFER_SENT,
            credential_definition_id=credential_definition_id,
            schema_id=credential_offer["schema_id"],
            credential_offer=credential_offer,
        )
        await credential_exchange.save(self.context.storage)

        credential_offer_message = CredentialOffer(offer_json=credential_offer)

        return credential_exchange, credential_offer_message

    async def receive_offer(self, credential_offer, connection_id):
        credential_exchange = CredentialExchange(
            connection_id=connection_id,
            initiator=CredentialExchange.INITIATOR_EXTERNAL,
            state=CredentialExchange.STATE_OFFER_RECEIVED,
            credential_definition_id=credential_offer["cred_def_id"],
            schema_id=credential_offer["schema_id"],
            credential_offer=credential_offer,
        )
        await credential_exchange.save(self.context.storage)

    async def create_request(self, credential_exchange_record: CredentialExchange):

        credential_definition_id = credential_exchange_record.credential_definition_id
        credential_offer = credential_exchange_record.credential_offer

        async with self.context.ledger:
            credential_definition = await self.context.ledger.get_credential_definition(
                credential_definition_id
            )

        credential_request = await self.context.holder.create_credential_request(
            credential_offer, credential_definition
        )

        credential_request_message = CredentialRequest(
            offer_json=credential_offer, credential_request_json=credential_request
        )

        credential_exchange_record.state = CredentialExchange.STATE_REQUEST_SENT
        credential_exchange_record.credential_request = credential_request
        await credential_exchange_record.save(self.context.storage)

        return credential_exchange_record, credential_request_message

    async def receive_request(self, credential_exchange_record: CredentialExchange, credential_request: dict):
        # TODO: just take in prover did, cred def id, and cred_req?
        #       do the hard work in here
        credential_exchange_record.credential_request = credential_request
        credential_exchange_record.state = CredentialExchange.STATE_REQUEST_RECEIVED
        await credential_exchange_record.save(self.context.storage)
