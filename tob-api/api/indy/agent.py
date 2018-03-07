import os

from von_agent.nodepool import NodePool
from von_agent.wallet import Wallet
from tob_api import hyperledger_indy
from von_agent.agents import Issuer as VonIssuer
from von_agent.agents import Verifier as VonVerifier
from von_agent.agents import HolderProver as VonHolderProver

import logging
logger = logging.getLogger(__name__)

WALLET_SEED = os.environ.get('INDY_WALLET_SEED')
if not WALLET_SEED or len(WALLET_SEED) is not 32:
    raise Exception('INDY_WALLET_SEED must be set and be 32 characters long.')


class Issuer:
    def __init__(self):
        config = hyperledger_indy.config()
        self.pool = NodePool(
            'the-org-book-issuer',
            config['genesis_txn_path'])

        issuer_type = 'default'
        issuer_config = '{"freshness_time":0}'
        issuer_creds = '{"key":""}'

        self.instance = VonIssuer(
            self.pool,
            WALLET_SEED,
            'TheOrgBook Issuer Wallet',
            issuer_type,
            issuer_config,
            issuer_creds
            '127.0.0.1',
            9703,
            'api/v0')

    async def __aenter__(self):
        await self.pool.open()
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()


class Verifier:
    def __init__(self):
        config = hyperledger_indy.config()
        self.pool = NodePool(
            'the-org-book-verifier',
            config['genesis_txn_path'])

        verifier_type = 'default'
        verifier_config = '{"freshness_time":0}'
        verifier_creds = '{"key":""}'

        self.instance = VonVerifier(
            self.pool,
            WALLET_SEED,
            'TheOrgBook Verifier Wallet',
            verifier_type,
            verifier_config,
            verifier_creds,
            '127.0.0.1',
            9703,
            'api/v0')

    async def __aenter__(self):
        await self.pool.open()
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()


class Holder:
    def __init__(self):
        config = hyperledger_indy.config()
        self.pool = NodePool(
            'the-org-book-holder',
            config['genesis_txn_path'])

        holder_type = 'default'
        holder_config = '{"freshness_time":0}'
        holder_creds = '{"key":""}'

        self.instance = VonHolderProver(
            self.pool,
            WALLET_SEED,
            'TheOrgBook Holder Wallet',
            holder_type,
            holder_config,
            holder_creds,
            '127.0.0.1',
            9703,
            'api/v0')

    async def __aenter__(self):
        await self.pool.open()
        instance = await self.instance.open()
        await self.instance.create_master_secret('secret')
        return instance

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()
