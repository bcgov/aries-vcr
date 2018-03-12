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
    def __init__(self):
        config = hyperledger_indy.config()
        self.pool = NodePool(
            'the-org-book-issuer',
            config['genesis_txn_path'])

        issuer_type   = 'virtual'
        issuer_config = {'freshness_time':0}
        issuer_creds  = {'key':''}

        self.instance = VonIssuer(
            self.pool,
            WALLET_SEED,
            'TheOrgBook Issuer Wallet',
            issuer_type,
            issuer_config,
            issuer_creds,
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

        verifier_type   = 'virtual'
        verifier_config = {'freshness_time':0}
        verifier_creds  = {'key':''}

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


class Holder(VonHolderProver):
    def __init__(self, legal_entity_id: str = None):
        self.my_config = hyperledger_indy.config()
        self.my_pool = NodePool(
            'the-org-book-holder',
            self.my_config['genesis_txn_path'])

        self.holder_type   = 'virtual'
        self.holder_config = {'freshness_time':0}
        self.holder_creds  = {'key':'', 'virtual_wallet':legal_entity_id}

        super().__init__(
            self.my_pool,
            Wallet(
                self.my_pool.name,
                WALLET_SEED,
                'TheOrgBook Holder Wallet',
                self.holder_type,
                self.holder_config,
                self.holder_creds,
            )
        )

    async def __aenter__(self):
        await self.my_pool.open()
        instance = await self.open()
        await instance.create_master_secret('secret')
        return instance

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)
        await self.close()
        await self.my_pool.close()


    async def create_master_secret(self, master_secret: str) -> None:
        logger.info("Enter >>>>>>>>>> TheOrgBook Holder called for create_master_secret()")
        await super(Holder, self).create_master_secret(master_secret)
        logger.info("Exit  <<<<<<<<<< TheOrgBook Holder called for create_master_secret()")

    async def store_claim_req(self, claim_offer_json: str, claim_def_json: str) -> str:
        logger.info("Enter >>>>>>>>>> TheOrgBook Holder called for store_claim_req()")
        ret = await super(Holder, self).store_claim_req(claim_offer_json, claim_def_json)
        logger.info("Exit  <<<<<<<<<< TheOrgBook Holder called for store_claim_req()")
        return ret

    async def store_claim(self, claim_json: str) -> None:
        logger.info("Enter >>>>>>>>>> TheOrgBook Holder called for store_claim()")
        await super(Holder, self).store_claim(claim_json)
        logger.info("Exit  <<<<<<<<<< TheOrgBook Holder called for store_claim()")

    async def create_proof(self, proof_req: dict, claims: dict, requested_claims: dict = None) -> str:
        logger.info("Enter >>>>>>>>>> TheOrgBook Holder called for create_proof()")
        ret = await super(Holder, self).create_proof(proof_req, claims, requested_claims)
        logger.info("Exit  <<<<<<<<<< TheOrgBook Holder called for create_proof()")
        return ret

    async def get_claims(self, proof_req_json: str, filt: dict = {}) -> (Set[str], str):
        logger.info("Enter >>>>>>>>>> TheOrgBook Holder called for get_claims()")
        claim_set = await super(Holder, self).get_claims(proof_req_json, filt)
        logger.info("Exit  <<<<<<<<<< TheOrgBook Holder called for get_claims()")
        return claim_set

    async def get_claim_by_referent(self, referents: set, requested_attrs: dict) -> str:
        logger.info("Enter >>>>>>>>>> TheOrgBook Holder called for get_claim_by_referent()")
        ret = await super(Holder, self).get_claim_by_referent(referents, requested_attrs)
        logger.info("Exit  <<<<<<<<<< TheOrgBook Holder called for get_claim_by_referent()")
        return ret

    async def reset_wallet(self) -> str:
        raise RuntimeError('Error attempt to reset wallet!!!!!')

    async def process_post(self, form: dict) -> str:
        logger.info("Enter >>>>>>>>>> TheOrgBook Holder called for process_post()")
        ret = await super(Holder, self).process_post(form)
        logger.info("Exit  <<<<<<<<<< TheOrgBook Holder called for process_post()")
        return ret
