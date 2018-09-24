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

from .config import (
    indy_general_wallet_config,
    indy_holder_wallet_config,
    indy_verifier_wallet_config,
)

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
        "INDY_GENESIS_URL": os.environ.get("GENESIS_URL"),
        "LEDGER_PROTOCOL_VERSION": os.environ.get("LEDGER_PROTOCOL_VERSION"),
    }


def indy_holder_id():
    return settings.INDY_HOLDER_ID


def indy_verifier_id():
    return settings.INDY_VERIFIER_ID


async def add_server_headers(request, response):
    host = os.environ.get("HOSTNAME")
    if host and "X-Served-By" not in response.headers:
        response.headers["X-Served-By"] = host


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
    no_headers = os.environ.get("DISABLE_SERVER_HEADERS")
    if not no_headers or no_headers == "false":
        app.on_response_prepare.append(add_server_headers)

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
