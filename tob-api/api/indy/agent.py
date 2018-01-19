from von_agent.nodepool import NodePool
from von_agent.agents import Issuer as VonIssuer
from von_agent.agents import Verifier as VonVerifier
from von_agent.agents import HolderProver as VonHolderProver

import logging
logger = logging.getLogger(__name__)


class Issuer:
    def __init__(self):
        self.pool = NodePool(
            'the-org-book-issuer',
            '/opt/app-root/genesis')

        self.instance = VonIssuer(
            self.pool,
            'the_org_book_issuer_000000000000',
            'TheOrgBook Issuer Wallet',
            None,
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
        self.pool = NodePool(
            'the-org-book-verifier',
            '/opt/app-root/genesis')

        self.instance = VonVerifier(
            self.pool,
            'the_org_book_verifier_0000000000',
            'TheOrgBook Verifier Wallet',
            None,
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
        self.pool = NodePool(
            'the-org-book-holder',
            '/opt/app-root/genesis')

        self.instance = VonHolderProver(
            self.pool,
            'the_org_book_holder_000000000000',
            'TheOrgBook Holder Wallet',
            None,
            '127.0.0.1',
            9703,
            'api/v0')

    async def __aenter__(self):
        await self.pool.open()
        await self.instance.create_master_secret('secret')
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()
