import os
import threading

from von_agent.nodepool import NodePool
from von_agent.wallet import Wallet
from tob_api import hyperledger_indy
from von_agent.agents import Issuer as VonIssuer
from von_agent.agents import Verifier as VonVerifier
from von_agent.agents import HolderProver as VonHolderProver
from typing import Set, Union

from api import apps

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
        wallet_name = 'TheOrgBook_Issuer_Wallet'

        issuer_type   = 'virtual'
        issuer_config = {'freshness_time':0}
        issuer_creds  = {'key':''}

        logger.debug("Issuer __init__>>> {} {} {}".format(issuer_type, issuer_config, issuer_creds))

        issuer_wallet = Wallet(
                self.pool,
                WALLET_SEED,
                wallet_name,
                issuer_type,
                issuer_config,
                issuer_creds)

        logger.debug("Issuer __init__>>> {} {} {}".format(issuer_type, issuer_config, issuer_creds))

        self.instance = VonIssuer(
            # self.pool,
            issuer_wallet
        )

    async def __aenter__(self):
        await self.pool.open()
        await self.instance.wallet.create()
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
        wallet_name = 'TheOrgBook_Verifier_Wallet'

        verifier_type   = 'virtual'
        verifier_config = {'freshness_time':0}
        verifier_creds  = {'key':''}

        logger.debug("Verifier __init__>>> {} {} {}".format(verifier_type, verifier_config, verifier_creds))

        verifier_wallet = Wallet(
                self.pool,
                WALLET_SEED,
                wallet_name,
                verifier_type,
                verifier_config,
                verifier_creds)

        logger.debug("Verifier __init__>>> {} {} {}".format(verifier_type, verifier_config, verifier_creds))

        self.instance = VonVerifier(
            # self.pool,
            verifier_wallet
        )

    async def __aenter__(self):
        await self.pool.open()
        await self.instance.wallet.create()
        return await self.instance.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)

        await self.instance.close()
        await self.pool.close()


class Holder:
    def __init__(self, legal_entity_id: str = None):
        config = hyperledger_indy.config()
        thread_id = threading.get_ident()
        self.pool = NodePool(
            'the-org-book-holder-' + str(thread_id),
            config['genesis_txn_path'])
        wallet_name = 'TheOrgBook_Holder_Wallet'

        holder_type   = os.environ.get('INDY_WALLET_TYPE')
        if holder_type == 'remote':
            wallet_name = wallet_name + "$$" + str(thread_id)
            holder_url = os.environ.get('INDY_WALLET_URL')
            holder_config = {'endpoint':holder_url,'ping':'schema/','auth':'api-token-auth/','keyval':'keyval/','freshness_time':0}
            holder_creds  = {'auth_token':apps.get_remote_wallet_token(),'virtual_wallet':legal_entity_id}
            logger.debug('Using remote Cfg: {} Creds: {}'.format(holder_config, holder_creds))
        else:
            # TODO force to virtual for now
            holder_type = 'virtual'
            holder_config = {'freshness_time':0}
            holder_creds  = {'key':'','virtual_wallet':legal_entity_id}
            logger.debug('Using virtual Cfg: {} Creds: {}'.format(holder_config, holder_creds))

        logger.debug("Holder __init__>>> {} {} {}".format(holder_type, holder_config, holder_creds))

        holder_wallet = Wallet(
                self.pool,
                WALLET_SEED,
                wallet_name,
                holder_type,
                holder_config,
                holder_creds)

        logger.debug("Holder __init__>>> {} {} {}".format(holder_type, holder_config, holder_creds))

        self.instance = VonHolderProver(
            # self.pool,
            holder_wallet
        )

    async def __aenter__(self):
        await self.pool.open()
        await self.instance.wallet.create()
        instance = await self.instance.open()
        # TODO should only create this once, and only in the root wallet (virtual_wallet == None)
        await self.instance.create_master_secret('secret')
        return instance

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(exc_type, exc_value, traceback)
        await self.instance.close()
        await self.pool.close()
