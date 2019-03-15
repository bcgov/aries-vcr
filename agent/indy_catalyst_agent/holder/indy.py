"""Indy issuer implementation."""

import json
import logging

import indy.anoncreds

from .base import BaseHolder


class IndyHolder(BaseHolder):
    """Indy holder class."""

    def __init__(self, wallet):
        """
        Initialize an IndyHolder instance.

        Args:
            wallet: IndyWallet instance

        """
        self.logger = logging.getLogger(__name__)
        self.wallet = wallet

    async def create_credential_request(self, credential_offer, credential_definition):
        """
        Create a credential offer for the given credential definition id.

        Args:
            credential_offer: The credential offer to create request for
            credential_definition: The credential definition to create an offer for

        Returns:
            A credential request

        """

        public_did = await self.wallet.get_public_did()

        credential_request_json, credential_request_metadata_json = await indy.anoncreds.prover_create_credential_req(
            self.wallet.handle,
            public_did.did,
            json.dumps(credential_offer),
            json.dumps(credential_definition),
            self.wallet.master_secret_id,
        )

        self.logger.debug(
            f"Created credential request. credential_request_json={credential_request_json} "
            + f"credential_request_metadata_json={credential_request_metadata_json}"
        )

        credential_request = json.loads(credential_request_json)

        return credential_request
