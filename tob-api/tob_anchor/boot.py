#
# Copyright 2017-2018 Government of Canada
# Public Services and Procurement Canada - buyandsell.gc.ca
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Importing this file causes the standard settings to be loaded
and a standard service manager to be created. This allows services
to be properly initialized before the webserver process has forked.
"""

import asyncio
import logging
import os
import platform

from django.conf import settings
import django.db
from wsgi import application

from vonx.common.eventloop import run_coro
from vonx.indy.manager import IndyManager

LOGGER = logging.getLogger(__name__)

STARTED = False

def get_genesis_path():
    if platform.system() == "Windows":
        txn_path = os.path.realpath("./genesis")
    else:
        txn_path = "/home/indy/genesis"
    txn_path = os.getenv("INDY_GENESIS_PATH", txn_path)
    return txn_path

def indy_client():
    if not STARTED:
        raise RuntimeError("Indy service is not running")
    return MANAGER.get_client()

def indy_env():
    return {
        "INDY_GENESIS_PATH": get_genesis_path(),
        "INDY_LEDGER_URL": os.environ.get("LEDGER_URL"),
    }

def indy_holder_id():
    return settings.INDY_HOLDER_ID

def indy_verifier_id():
    return settings.INDY_VERIFIER_ID

async def init_app(on_startup=None, on_cleanup=None):
    from aiohttp.web import Application
    from aiohttp_wsgi import WSGIHandler
    from tob_anchor.urls import get_routes

    wsgi_handler = WSGIHandler(application)
    app = Application()
    app["manager"] = MANAGER
    app.router.add_routes(get_routes())
    # all other requests forwarded to django
    app.router.add_route("*", "/{path_info:.*}", wsgi_handler)

    if on_startup:
        app.on_startup.append(on_startup)
    if on_cleanup:
        app.on_cleanup.append(on_cleanup)

    return app

def run_django(proc, *args) -> asyncio.Future:
    def runner(proc, *args):
        try:
            ret = proc(*args)
            return ret
        finally:
            django.db.connections.close_all()
    return asyncio.get_event_loop().run_in_executor(None, runner, proc, *args)

def run_reindex():
    from django.core.management import call_command
    batch_size = os.getenv("SOLR_BATCH_SIZE", 500)
    call_command("update_index", "--max-retries=5", "--batch-size={}".format(batch_size))
    update_suggester()

def update_suggester():
    from api_v2.suggest import SuggestManager
    SuggestManager().rebuild()

def run_migration():
    from django.core.management import call_command
    call_command("migrate")

def pre_init(proc=False):
    global MANAGER, STARTED
    if proc:
        MANAGER.start_process()
    else:
        MANAGER.start()
    STARTED = True
    try:
        run_coro(register_services())
    except:
        LOGGER.exception("Error during Indy initialization:")
        MANAGER.stop()
        STARTED = False
        raise

def indy_general_wallet_config():
    # wallet configuration
    # - your choice of postgres or sqlite at the moment
    # - defaults to sqlite for compatibility
    wallet_type = os.environ.get('WALLET_TYPE')
    wallet_type = wallet_type.lower() if wallet_type else 'sqlite'

    wallet_encryp_key = os.environ.get('WALLET_ENCRYPTION_KEY') or "key"

    ret = {"type": wallet_type}

    if wallet_type == 'postgres':
        LOGGER.info("Using Postgres storage ...")

        # postgresql wallet-db configuration
        wallet_host = os.environ.get('POSTGRESQL_WALLET_HOST')
        if not wallet_host:
            raise ValueError('POSTGRESQL_WALLET_HOST must be set.')
        wallet_port = os.environ.get('POSTGRESQL_WALLET_PORT')
        if not wallet_port:
            raise ValueError('POSTGRESQL_WALLET_PORT must be set.')
        wallet_user = os.environ.get('POSTGRESQL_WALLET_USER')
        if not wallet_user:
            raise ValueError('POSTGRESQL_WALLET_USER must be set.')
        wallet_password = os.environ.get('POSTGRESQL_WALLET_PASSWORD')
        if not wallet_password:
            raise ValueError('POSTGRESQL_WALLET_PASSWORD must be set.')
        wallet_admin_user = 'postgres'
        wallet_admin_password = os.environ.get('POSTGRESQL_WALLET_ADMIN_PASSWORD')

        # TODO pass in as env parameter - key for encrypting the wallet contents

        ret["params"] = {
            "storage_config": {"url": "{}:{}".format(wallet_host, wallet_port)},
        }
        stg_creds = {"account": wallet_user, "password": wallet_password}
        if wallet_admin_password:
            stg_creds["admin_account"] = wallet_admin_user
            stg_creds["admin_password"] = wallet_admin_password
        ret["access_creds"] = {
            "key": wallet_encryp_key,
            "storage_credentials": stg_creds,
            "key_derivation_method": "ARGON2I_MOD",
        }

    elif wallet_type == 'sqlite':
        LOGGER.info("Using Sqlite storage ...")
        ret["access_creds"] = {"key": wallet_encryp_key}
    else:
        raise ValueError('Unknown WALLET_TYPE: {}'.format(wallet_type))

    return ret

def indy_holder_wallet_config(wallet_cfg: dict):
    wallet_seed = os.environ.get('INDY_WALLET_SEED')
    if not wallet_seed or len(wallet_seed) is not 32:
        raise ValueError('INDY_WALLET_SEED must be set and be 32 characters long.')

    if wallet_cfg['type'] == 'postgres':
        return {
            "name": "tob_holder",
            "seed": wallet_seed,
            "type": "postgres",
            "params": wallet_cfg["params"],
            "access_creds": wallet_cfg["access_creds"],
        }
    return {
        "name": "TheOrgBook_Holder_Wallet",
        "seed": wallet_seed,
        "access_creds": wallet_cfg["access_creds"],
    }

def indy_verifier_wallet_config(wallet_cfg: dict):
    verifier_seed = "tob-verifier-wallet-000000000001"

    if wallet_cfg['type'] == 'postgres':
        return {
            "name": "tob_verifier",
            "seed": verifier_seed,
            "type": "postgres",
            "params": wallet_cfg["params"],
            "access_creds": wallet_cfg["access_creds"],
        }
    return {
        "name": "TheOrgBook_Verifier_Wallet",
        "seed": verifier_seed,
        "access_creds": wallet_cfg["access_creds"],
    }

async def register_services():

    await asyncio.sleep(2) # temp fix for messages being sent before exchange has started

    client = indy_client()
    wallet_config = indy_general_wallet_config()

    LOGGER.info("Registering holder service")
    holder_wallet_id = await client.register_wallet(
        indy_holder_wallet_config(wallet_config))
    LOGGER.debug("Indy holder wallet id: %s", holder_wallet_id)

    holder_id = await client.register_holder(holder_wallet_id, {
        "id": indy_holder_id(),
        "name": "TheOrgBook Holder",
    })
    LOGGER.debug("Indy holder id: %s", holder_id)

    LOGGER.info("Registering verifier service")
    verifier_wallet_id = await client.register_wallet(
        indy_verifier_wallet_config(wallet_config))
    LOGGER.debug("Indy verifier wallet id: %s", verifier_wallet_id)

    verifier_id = await client.register_verifier(verifier_wallet_id, {
        "id": indy_verifier_id(),
        "name": "TheOrgBook Verifier",
    })
    LOGGER.info("Indy verifier id: %s", verifier_id)

    await client.sync()
    LOGGER.debug("Indy client synced")
    LOGGER.debug(await client.get_status())

def shutdown():
    MANAGER.stop()


MANAGER = IndyManager(indy_env())
