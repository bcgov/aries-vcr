# This file supercedes the normal s2i boot process, which is to
# run manage.py migrate and then invoke gunicorn.

import argparse
import os

import django
from django.conf import settings
import requests
from aiohttp import web

from app.utils.boot import init_app, run_django, run_migration, run_reindex

parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument("--host", default=os.getenv("HTTP_HOST"))
parser.add_argument("-p", "--port", default=os.getenv("HTTP_PORT"))
parser.add_argument("-s", "--socket", default=os.getenv("SOCKET_PATH"))


if __name__ == "__main__":
    django.setup()

    disable_migrate = os.environ.get("DISABLE_MIGRATE", "false")
    disconnected = os.environ.get("INDY_DISABLED", "false")
    skip_indexing = os.environ.get("SKIP_INDEXING_ON_STARTUP", "false")

    if not disable_migrate or disable_migrate == "false":
        do_reindex = False
        if not skip_indexing or skip_indexing == "false":
            os.environ["SKIP_INDEXING_ON_STARTUP"] = "active"
            do_reindex = True
        run_migration()
        if do_reindex:
            # queue in current asyncio loop
            run_django(run_reindex)

    # Make agent connection to self to send self presentation requests later
    response = requests.get(
        f"{settings.AGENT_ADMIN_URL}/connections"
        + f"?alias={settings.AGENT_SELF_CONNECTION_ALIAS}",
        headers=settings.ADMIN_REQUEST_HEADERS,
    )
    connections = response.json()

    # We only need to form a self connection once
    if not connections["results"]:
        response = requests.post(
            f"{settings.AGENT_ADMIN_URL}/connections/create-invitation"
            + f"?alias={settings.AGENT_SELF_CONNECTION_ALIAS}",
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        response_body = response.json()
        requests.post(
            f"{settings.AGENT_ADMIN_URL}/connections/receive-invitation",
            json=response_body["invitation"],
            headers=settings.ADMIN_REQUEST_HEADERS,
        )

    args = parser.parse_args()
    if not args.socket and not args.port:
        args.port = 8080

    app = init_app(None)
    web.run_app(
        app, host=args.host, port=args.port, path=args.socket, handle_signals=True
    )
