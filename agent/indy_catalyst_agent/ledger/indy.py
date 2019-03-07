"""Indy ledger implementation."""

import json
import logging

from indy.error import IndyError, ErrorCode
import indy.ledger, indy.pool

from .base import BaseLedger
from .error import ClosedPoolError, LedgerTransactionError

GENESIS_TRANSACTION_PATH = "/tmp/indy_genesis_transactions"


class IndyLedger(BaseLedger):
    """Indy ledger class."""

    def __init__(self, name, wallet, genesis_transactions):
        """
        Initialize an IndyLedger instance.

        Args:
            wallet: IndyWallet instance
            genesis_transactions: String of genesis transactions

        """
        self.name = name
        self.wallet = wallet

        # indy-sdk requires a file but it's only used once to bootstrap
        # the connection so we take a string instead of create a tmp file
        with open(GENESIS_TRANSACTION_PATH, "w") as genesis_file:
            genesis_file.write(self.genesis_transactions)

        self.logger = logging.getLogger(__name__)

    async def __aenter__(self) -> "IndyLedger":
        """
        Context manager entry.

        Returns:
            The current instance

        """
        pool_config = json.dumps({"genesis_txn": GENESIS_TRANSACTION_PATH})
        await indy.pool.create_pool_ledger_config(self.name, pool_config)
        self.pool_handle = await indy.pool.open_pool_ledger(self.name)
        return self

    async def __aexit__(self):
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

        request_result_json = await indy.ledger.sign_and_submit_request(
            self.pool_handle, self.wallet.handle, self.did, request_json
        )
        request_result = json.loads(request_result_json)

        if request_result.get("op", "") in ("REQNACK", "REJECT"):
            raise LedgerTransactionError(
                f"Ledger rejected transaction request: {request_result['reason']}"
            )

        return request_result
