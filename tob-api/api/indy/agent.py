import os

from von_agent.nodepool import NodePool
from von_agent.wallet import Wallet
from tob_api import hyperledger_indy
from von_agent.agents import Issuer as VonIssuer
from von_agent.agents import Verifier as VonVerifier
from von_agent.agents import HolderProver as VonHolderProver
from typing import Set, Union

import logging
logger = logging.getLogger(__name__)

WALLET_SEED = os.environ.get('INDY_WALLET_SEED')
if not WALLET_SEED or len(WALLET_SEED) is not 32:
    raise Exception('INDY_WALLET_SEED must be set and be 32 characters long.')


class Issuer:
    async def __init__(self):
        config = hyperledger_indy.config()
        self.pool = NodePool(
            'the-org-book-issuer',
            config['genesis_txn_path'])

        issuer_type   = 'virtual'
        issuer_config = {'freshness_time':0}
        issuer_creds  = {'key':''}

        issuer_wallet = Wallet(
                self.pool.name,
                WALLET_SEED,
                'TheOrgBookIssuerWallet',
                issuer_type,
                issuer_config,
                issuer_creds)
        await issuer_wallet.create()

        self.instance = VonIssuer(
            self.pool,
            issuer_wallet
        )

    async def __aenter__(self):
        await self.pool.open()
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()


class Verifier:
    async def __init__(self):
        config = hyperledger_indy.config()
        self.pool = NodePool(
            'the-org-book-verifier',
            config['genesis_txn_path'])

        verifier_type   = 'virtual'
        verifier_config = {'freshness_time':0}
        verifier_creds  = {'key':''}

        verifier_wallet = Wallet(
                self.pool.name,
                WALLET_SEED,
                'TheOrgBookVerifierWallet',
                verifier_type,
                verifier_config,
                verifier_creds)
        await verifier_wallet.create()

        self.instance = VonVerifier(
            self.pool,
            verifier_wallet
        )

    async def __aenter__(self):
        await self.pool.open()
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()


class Holder:
    async def __init__(self, legal_entity_id: str = None):
        config = hyperledger_indy.config()
        self.pool = NodePool(
            'the-org-book-holder',
            config['genesis_txn_path'])

        holder_type   = 'virtual'
        holder_config = {'freshness_time':0}
        holder_creds  = {'key':'', 'virtual_wallet':legal_entity_id}

        holder_wallet = Wallet(
                self.pool.name,
                WALLET_SEED,
                'TheOrgBookHolderWallet',
                holder_type,
                holder_config,
                holder_creds)
        await holder_wallet.create()

        self.instance = VonHolderProver(
            self.pool,
            holder_wallet
        )

    async def __aenter__(self):
        await self.pool.open()
        instance = await self.instance.open()
        # TODO should only create this once, and only in the root wallet (virtual_wallet == None)
        await self.instance.create_master_secret('secret')
        return instance

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)
        await self.instance.close()
        await self.pool.close()
