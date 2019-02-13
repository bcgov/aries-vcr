"""
Connection management
"""

import json
import logging

import aiohttp

from .error import BaseError
from .messaging.connections.messages.connection_invitation import ConnectionInvitation
from .messaging.connections.messages.connection_request import ConnectionRequest
from .messaging.connections.messages.connection_response import ConnectionResponse
from .messaging.request_context import RequestContext
from .models.connection_detail import ConnectionDetail
from .models.connection_target import ConnectionTarget
from .models.thread_decorator import ThreadDecorator
from .storage import StorageRecord, StorageNotFoundError
from .wallet.util import bytes_to_b64

from von_anchor.a2a import DIDDoc
from von_anchor.a2a.publickey import PublicKey, PublicKeyType
from von_anchor.a2a.service import Service


class ConnectionError(BaseError):
    pass


class ConnectionManager:
    def __init__(self, context: RequestContext):
        self._context = context
        self._logger = logging.getLogger(__name__)

    @property
    def context(self) -> RequestContext:
        """
        Accessor for the current request context
        """
        return self._context

    async def create_invitation(self, label: str, my_endpoint: str, seed: str = None, metadata: dict = None) -> ConnectionInvitation:
        """
        Generate new connection invitation.
        This interaction represents an out-of-band communication channel. In the future and in
        practice, these sort of invitations will be received over any number of channels such as
        SMS, Email, QR Code, NFC, etc.
        Structure of an invite message:
            {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
                "label": "Alice",
                "did": "did:sov:QmWbsNYhMrjHiqZDTUTEJs"
            }
        Or, in the case of a peer DID:
            {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
                "label": "Alice",
                "did": "did:peer:oiSqsNYhMrjHiqZDTUthsw",
                "recipient_keys": ["8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K"],
                "serviceEndpoint": "https://example.com/endpoint"
            }
        Currently, only peer DID is supported.
        """
        self._logger.debug("Creating invitation")

        # Create and store new connection key
        connection_key = await self.context.wallet.create_signing_key(
            seed=seed, metadata=metadata)
            # may want to store additional metadata on the key (creation date etc.)

        # Create connection invitation message
        invitation = ConnectionInvitation(
            label=label,
            recipient_keys=[connection_key.verkey],
            endpoint=my_endpoint,
        )
        return invitation
    
    async def send_invitation(self, invitation: ConnectionInvitation, endpoint: str):
        """
        Deliver an invitation to an HTTP endpoint
        """
        self._logger.debug(f"Sending invitation to {endpoint}")
        invite_json = json.dumps(invitation.serialize())
        invite_b64 = bytes_to_b64(invite_json.encode("ascii"), urlsafe=True)
        async with aiohttp.ClientSession() as session:
            await session.get(endpoint, params={"c_i": invite_b64})

    async def store_invitation(
            self,
            invitation: ConnectionInvitation,
            received: bool,
            tags: dict = None) -> str:
        """
        Save an invitation for acceptance/rejection and later processing
        """
        # may want to generate another unique ID, or use the message ID instead of the key
        invitation_id = invitation.recipient_keys[0]

        await self.context.storage.add_record(
            StorageRecord(
                "received_invitation" if received else "sent_invitation",
                json.dumps(invitation.serialize()),
                tags,
                invitation_id,
            )
        )
        self._logger.debug("Stored %s invitation: %s", "incoming" if received else "outgoing", invitation_id)
        return invitation_id

    async def find_invitation(self, invitation_id: str, received: bool) -> (ConnectionInvitation, dict):
        """
        Locate a previously-received invitation
        """
        self._logger.debug("Looking up %s invitation: %s", "incoming" if received else "outgoing", invitation_id)
        # raises exception if not found
        result = await self.context.storage.get_record(
            "received_invitation" if received else "sent_invitation",
            invitation_id,
        )
        invitation = ConnectionInvitation.deserialize(result.value)
        return invitation, result.tags

    async def remove_invitation(self, invitation_id: str):
        """
        Remove a previously-stored invitation
        """
        # raises exception if not found
        await self.context.storage.delete_record(
            "invitation",
            invitation_id,
        )

    async def accept_invitation(
            self,
            invitation: ConnectionInvitation,
            my_label: str = None,
            my_endpoint: str = None) -> (ConnectionRequest, ConnectionTarget):
        """
        Create a new connection request for a previously-received invitation
        """

        their_label = invitation.label
        their_connection_key = invitation.recipient_keys[0]
        their_endpoint = invitation.endpoint

        # Create my information for connection
        my_info = await self.context.wallet.create_local_did(
            None, None, {
                "their_label": their_label,
                "their_endpoint": their_endpoint,
            }
        )
        if not my_label:
            my_label = self.context.default_label
        if not my_endpoint:
            my_endpoint = self.context.default_endpoint

        did_doc = DIDDoc(did=my_info.did)
        controller = my_info.did
        value = my_info.verkey
        pk = PublicKey(my_info.did, "1", PublicKeyType.ED25519_SIG_2018, controller, value, False)
        did_doc.verkeys.append(pk)
        service = Service(my_info.did, "indy", "IndyAgent", my_endpoint)
        did_doc.services.append(service)

        # Create connection request message
        request = ConnectionRequest(
            label=my_label,
            connection=ConnectionDetail(did=my_info.did, did_doc=did_doc),
        )

        # Store message so that response can be processed
        await self.context.storage.add_record(
            StorageRecord(
                "connection_request",
                json.dumps(request.serialize()),
                {},
                request._id,
            )
        )

        # request must be sent to their_endpoint using their_connection_key, from my_info.verkey
        target = ConnectionTarget(
            endpoint=their_endpoint,
            recipient_keys=[their_connection_key],
            sender_key=my_info.verkey,
        )
        return request, target

    async def find_request(self, request_id: str) -> ConnectionRequest:
        """
        Locate a previously saved connection request
        """
        # raises exception if not found
        result = await self.context.storage.get_record(
            "connection_request",
            request_id,
        )
        request = ConnectionRequest.deserialize(result.value)
        return request

    async def remove_request(self, request_id: str):
        """
        Remove a previously-stored connection request
        """
        # raises exception if not found
        await self.context.storage.delete_record(
            "connection_request",
            request_id,
        )

    async def accept_request(
            self,
            request: ConnectionRequest,
            my_endpoint: str = None) -> (ConnectionResponse, ConnectionTarget):
        """
        Create a connection response for a received connection request
        """

        invitation = None
        if not self.context.recipient_did_public:
            connection_key = self.context.recipient_verkey
            try:
                invitation, _inv_tags = await self.find_invitation(connection_key, False)
            except StorageNotFoundError:
                #temporarily disabled
                #raise ConnectionError("No invitation found for pairwise connection")
                pass
        self._logger.debug(f"Found invitation: {invitation}")
        if not my_endpoint:
            my_endpoint = self.context.default_endpoint

        their_label = request.label
        their_did = request.connection.did
        conn_did_doc = request.connection.did_doc
        their_verkey = conn_did_doc.verkeys[0].value # may be different from self.context.sender_verkey
        their_endpoint = conn_did_doc.services[0].endpoint

        # Create a new pairwise record with a newly-generated local DID
        pairwise = await self.context.wallet.create_pairwise(
            their_did,
            their_verkey,
            None,
            {
                "label": their_label,
                "endpoint": their_endpoint,
                # TODO: store established & last active dates
            }
        )

        my_did = pairwise.my_did
        did_doc = DIDDoc(did=my_did)
        controller = my_did
        value = pairwise.my_verkey
        pk = PublicKey(my_did, "1", PublicKeyType.ED25519_SIG_2018, controller, value, False)
        did_doc.verkeys.append(pk)
        service = Service(my_did, "indy", "IndyAgent", my_endpoint)
        did_doc.services.append(service)

        response = ConnectionResponse(
            connection=ConnectionDetail(did=my_did, did_doc=did_doc),
        )
        if request._id:
            response._thread = ThreadDecorator(thid=request._id)
        await response.sign_field(
            "connection",
            self.context.recipient_verkey,
            self.context.wallet
        )
        self._logger.debug(f"Created connection response for {their_did}")

        # response must be sent to their_endpoint, packed with their_verkey and pairwise.my_verkey
        target = ConnectionTarget(
            endpoint=their_endpoint,
            recipient_keys=[their_verkey],
            sender_key=pairwise.my_verkey,
        )
        return response, target

    async def accept_response(self, response: ConnectionResponse) -> ConnectionTarget:
        """
        Process a ConnectionResponse message by looking up
        the connection request and setting up the pairwise connection
        """

        request_id = response._thread.thid
        request = await self.find_request(request_id)

        my_did = request.connection.did
        their_did = response.connection.did
        conn_did_doc = request.connection.did_doc
        their_verkey = conn_did_doc.verkeys[0].value
        their_endpoint = conn_did_doc.services[0].endpoint

        my_info = await self.context.wallet.get_local_did(my_did)
        their_label = my_info.metadata.get("their_label")
        if not their_endpoint:
            their_endpoint = my_info.metadata.get("their_endpoint")
        if not their_label:
            # local DID not associated with a connection
            raise ConnectionError()

        # update local DID metadata to mark connection as accepted, prevent multiple responses?
        # may also set a creation time on the local DID to allow request expiry

        # In the final implementation, a signature will be provided to verify changes to
        # the keys and DIDs to be used long term in the relationship.
        # Both the signature and signature check are omitted for now until specifics of the
        # signature are decided.

        # Create a new pairwise record associated with our previously-generated local DID
        # Note: WalletDuplicateError will be raised if their_did already has a connection
        pairwise = await self.context.wallet.create_pairwise(
            their_did,
            their_verkey,
            my_did,
            {
                "label": their_label,
                "endpoint": their_endpoint,
                # TODO: store established & last active dates
            }
        )
        self._logger.debug(f"Accepted connection response from {their_did}")

        target = ConnectionTarget(
            endpoint=their_endpoint,
            recipient_keys=[their_verkey],
            sender_key=pairwise.my_verkey,
        )
        # Caller may wish to send a Trust Ping to verify the endpoint
        # and confirm the connection
        return target
