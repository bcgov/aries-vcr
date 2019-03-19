"""Indy issuer implementation."""

import json
import logging

from hashlib import sha256

import indy.anoncreds

from ..error import BaseError
from .base import BaseIssuer


class IssuerError(BaseError):
    """Generic issuer error."""


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

    async def create_credential(
        self, schema, credential_offer, credential_request, credential_values
    ):

        encoded_values = {}
        schema_attributes = schema["attrNames"]
        for attribute in schema_attributes:

            # Force every attribute present in schema to be set. Extraneous attribute names are ignored.
            try:
                credential_value = credential_values[attribute]
            except KeyError:
                raise IssuerError(
                    "Provided credential values is missed a value for the schema attribute "
                    + f"'{attribute}'"
                )

            credential_value_string = str(credential_value)
            encoded_values[attribute] = {}

            # If the value can be represented as an integer, we set the raw and encoded values
            # to the integer representation as a string - str(int(val))
            try:
                encoded_credential_value = int(credential_value)
                encoded_credential_value_string = str(encoded_credential_value)
                credential_value_string = encoded_credential_value_string
            except ValueError:
                # If the value can't be represented as an integer, we encode the raw value as an integer
                # representation as the SHA256 hash value
                credential_value_bytes = credential_value.encode()
                credential_value_hash_bytes = sha256(credential_value_bytes).digest()
                credential_value_as_int = int.from_bytes(
                    credential_value_hash_bytes, byteorder="big"
                )
                encoded_credential_value_string = str(credential_value_as_int)

            encoded_values[attribute]["raw"] = credential_value_string
            encoded_values[attribute]["encoded"] = encoded_credential_value_string

        (
            credential_json,
            credential_revocation_id,
            _,
        ) = await indy.anoncreds.issuer_create_credential(
            self.wallet.handle,
            json.dumps(credential_offer),
            json.dumps(credential_request),
            json.dumps(encoded_values),
            None,
            None,
        )

        return json.loads(credential_json), credential_revocation_id
