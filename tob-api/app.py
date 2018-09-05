# This file supercedes the normal s2i boot process, which is to
# run manage.py migrate and then invoke gunicorn.

import argparse
import os

from aiohttp import web
from tob_anchor.boot import MANAGER, init_app, pre_init, run_migration

parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--host', default=os.getenv('HTTP_HOST'))
parser.add_argument('-p', '--port', default=os.getenv('HTTP_PORT'))
parser.add_argument('-s', '--socket', default=os.getenv('SOCKET_PATH'))

if __name__ == '__main__':
    if not os.getenv("DISABLE_MIGRATE"):
        run_migration()

    args = parser.parse_args()
    if not args.socket and not args.port:
        args.port = 8080

    pre_init()

    web.run_app(
        init_app(),
        host=args.host, port=args.port, path=args.socket,
        handle_signals=True
    )
