"""Indy ledger implementation."""

import asyncio
import json
import logging
import tempfile

from time import time
from os import path


from indy.error import IndyError, ErrorCode
import indy.ledger, indy.pool, indy.anoncreds

from .base import BaseLedger
from .error import ClosedPoolError, LedgerTransactionError

GENESIS_TRANSACTION_PATH = tempfile.gettempdir()
GENESIS_TRANSACTION_PATH = path.join(
    GENESIS_TRANSACTION_PATH, "indy_genesis_transactions.txt"
)


class IndyLedger(BaseLedger):
    """Indy ledger class."""

    def __init__(self, name, wallet, genesis_transactions):
        """
        Initialize an IndyLedger instance.

        Args:
            wallet: IndyWallet instance
            genesis_transactions: String of genesis transactions

        """
        self.logger = logging.getLogger(__name__)

        self.name = name
        self.wallet = wallet

        # TODO: ensure wallet type is indy

        # indy-sdk requires a file but it's only used once to bootstrap
        # the connection so we take a string instead of create a tmp file
        with open(GENESIS_TRANSACTION_PATH, "w") as genesis_file:
            genesis_file.write(genesis_transactions)

    async def __aenter__(self) -> "IndyLedger":
        """
        Context manager entry.

        Returns:
            The current instance

        """
        pool_config = json.dumps({"genesis_txn": GENESIS_TRANSACTION_PATH})
        await indy.pool.set_protocol_version(2)

        try:
            await indy.pool.create_pool_ledger_config(self.name, pool_config)
        except Exception as e:
            self.logger.error(e)

        self.pool_handle = await indy.pool.open_pool_ledger(self.name, "{}")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Context manager exit."""
        await indy.pool.close_pool_ledger(self.pool_handle)
        self.pool_handle = None

    async def _submit(self, request_json: str) -> str:
        """
        Sign and submit request to ledger.

        Args:
            request_json: The json string to submit

        """

        if not self.pool_handle:
            raise ClosedPoolError(
                "Cannot sign and submit request to closed pool {}".format(
                    self.pool.name
                )
            )

        public_did = await self.wallet.get_public_did()

        request_result_json = await indy.ledger.sign_and_submit_request(
            self.pool_handle, self.wallet.handle, public_did.did, request_json
        )
        request_result = json.loads(request_result_json)

        if request_result.get("op", "") in ("REQNACK", "REJECT"):
            raise LedgerTransactionError(
                f"Ledger rejected transaction request: {request_result['reason']}"
            )

        return request_result

    async def send_schema(self, schema_name, schema_version, attribute_names: list):
        """
        Send schema to ledger.

        Args:
            schema_name: The schema name
            schema_version: The schema version
            attribute_names: A list of schema attributes

        """

        public_did = await self.wallet.get_public_did()

        schema_id, schema_json = await indy.anoncreds.issuer_create_schema(
            public_did.did, schema_name, schema_version, json.dumps(attribute_names)
        )

        req_json = await indy.ledger.build_schema_request(public_did.did, schema_json)
        await self._submit(req_json)

        return schema_id, await self.get_schema(schema_id)

    async def get_schema(self, schema_id):
        """
        Get schema from ledger.

        Args:
            schema_id: The schema id to retrieve

        """

        public_did = await self.wallet.get_public_did()
        req_json = await indy.ledger.build_get_schema_request(public_did.did, schema_id)
        response = await self._submit(req_json)
        return response
