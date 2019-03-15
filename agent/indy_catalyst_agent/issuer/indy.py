"""Indy issuer implementation."""

import json
import logging

import indy.anoncreds

from .base import BaseIssuer


class IndyIssuer(BaseIssuer):
    """Indy issuer class."""

    def __init__(self, wallet):
        """
        Initialize an IndyLedger instance.

        Args:
            wallet: IndyWallet instance

        """
        self.logger = logging.getLogger(__name__)
        self.wallet = wallet

    async def create_credential_offer(self, credential_definition_id):
        """
        Create a credential offer for the given credential definition id.

        Args:
            credential_definition_id: The credential definition to create an offer for

        Returns:
            A credential offer
            
        """
        credential_offer_json = await indy.anoncreds.issuer_create_credential_offer(
            self.wallet.handle, credential_definition_id
        )

        credential_offer = json.loads(credential_offer_json)

        return credential_offer
