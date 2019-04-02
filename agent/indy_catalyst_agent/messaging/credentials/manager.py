"""Classes to manage credentials."""

import logging

from ..request_context import RequestContext
from ...error import BaseError

from ..connections.models.connection_record import ConnectionRecord

from .messages.credential_issue import CredentialIssue
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
        """
        Create an offer.

        Args:
            credential_definition_id: Credential definition id for offer
            connection_id: Connection to create offer for

        Returns:
            A tuple (credential_exchange, credential_offer_message)

        """
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
        """
        Receive a credential offer.

        Args:
            credential_offer: Credential offer to receive
            connection_id: Connection to receive offer on

        """
        credential_exchange = CredentialExchange(
            connection_id=connection_id,
            initiator=CredentialExchange.INITIATOR_EXTERNAL,
            state=CredentialExchange.STATE_OFFER_RECEIVED,
            credential_definition_id=credential_offer["cred_def_id"],
            schema_id=credential_offer["schema_id"],
            credential_offer=credential_offer,
        )
        await credential_exchange.save(self.context.storage)

    async def create_request(
        self,
        credential_exchange_record: CredentialExchange,
        connection_record: ConnectionRecord,
    ):
        """
        Create a credential request.

        Args:
            credential_exchange_record: Credential exchange to create request for
            connection_record: Connection to create the request for

        Return:
            A tuple (credential_exchange_record, credential_request_message)

        """

        credential_definition_id = credential_exchange_record.credential_definition_id
        credential_offer = credential_exchange_record.credential_offer

        did = connection_record.my_did

        async with self.context.ledger:
            credential_definition = await self.context.ledger.get_credential_definition(
                credential_definition_id
            )

        credential_request = await self.context.holder.create_credential_request(
            credential_offer, credential_definition, did
        )

        credential_request_message = CredentialRequest(
            offer_json=credential_offer, credential_request_json=credential_request
        )

        credential_exchange_record.state = CredentialExchange.STATE_REQUEST_SENT
        credential_exchange_record.credential_request = credential_request
        await credential_exchange_record.save(self.context.storage)

        return credential_exchange_record, credential_request_message

    async def receive_request(self, credential_request: dict):
        """
        Receive a credential request.

        Args:
            credential_request: Credential request to receive

        """

        credential_definition_id = credential_request["cred_def_id"]

        prover_did = credential_request["prover_did"]
        connection_record = await ConnectionRecord.retrieve_by_did(
            self.context.storage, their_did=prover_did
        )

        # TODO: We need a way to identify the record we are concerned with
        #       deterministically We can probably use the thread_id
        #       once that is available. Until then, if multiple credential
        #       negotiations are active at the same time, and error will be raised
        credential_exchange_record = await CredentialExchange.retrieve_by_tag_filter(
            self.context.storage,
            tag_filter={
                "state": CredentialExchange.STATE_OFFER_SENT,
                "credential_definition_id": credential_definition_id,
                "connection_id": connection_record.connection_id,
            },
        )

        credential_exchange_record.credential_request = credential_request
        credential_exchange_record.state = CredentialExchange.STATE_REQUEST_RECEIVED
        await credential_exchange_record.save(self.context.storage)

    async def issue_credential(
        self, credential_exchange_record: CredentialExchange, credential_values: dict
    ):
        """
        Issue a credential.

        Args:
            credential_exchange_record: The credential exchange we are issuing a
                credential for
            credential_values: dict of credential values

        Returns:
            Tuple: (Updated credential exchange record, credential message obj)

        """

        schema_id = credential_exchange_record.schema_id
        credential_offer = credential_exchange_record.credential_offer
        credential_request = credential_exchange_record.credential_request

        async with self.context.ledger:
            schema = await self.context.ledger.get_schema(schema_id)

        (
            credential,
            credential_revocation_id,
        ) = await self.context.issuer.create_credential(
            schema, credential_offer, credential_request, credential_values
        )

        credential_exchange_record.state = CredentialExchange.STATE_ISSUED
        await credential_exchange_record.save(self.context.storage)

        credential_message = CredentialIssue(
            credential_json=credential, revocation_registry_id=credential_revocation_id
        )

        return credential_exchange_record, credential_message

    async def store_credential(self, credential):
        """
        Store a credential in the wallet.

        Args:
            credential: credential to store

        Returns:
            credential wallet id

        """
        async with self.context.ledger:
            credential_definition = await self.context.ledger.get_credential_definition(
                credential["cred_def_id"]
            )

        credential_id = await self.context.holder.store_credential(
            credential_definition, credential
        )

        # TODO: We need a way to identify and retrieve the current credential
        #       exchange record so that we can set the state to "stored".
        #       We can likely use the thread id once that is generalized
        #       and available on the request context

        return credential_id
