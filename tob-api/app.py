# This file supercedes the normal s2i boot process, which is to
# run manage.py migrate and then invoke gunicorn.

import argparse
import os

from aiohttp import web
import django
from tob_anchor.boot import (
    MANAGER, init_app, pre_init, run_django, run_reindex, run_migration,
    update_suggester,
)

parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--host', default=os.getenv('HTTP_HOST'))
parser.add_argument('-p', '--port', default=os.getenv('HTTP_PORT'))
parser.add_argument('-s', '--socket', default=os.getenv('SOCKET_PATH'))


if __name__ == '__main__':
    django.setup()

    disable_migrate = os.environ.get('DISABLE_MIGRATE', 'false')
    disconnected = os.environ.get('INDY_DISABLED', 'false')
    skip_indexing = os.environ.get('SKIP_INDEXING_ON_STARTUP', 'false')

    if not disable_migrate or disable_migrate == 'false':
        do_reindex = False
        if not skip_indexing or skip_indexing == 'false':
            os.environ['SKIP_INDEXING_ON_STARTUP'] = 'active'
            do_reindex = True
        run_migration()
        if do_reindex:
            # queue in current asyncio loop
            run_django(run_reindex)
        elif skip_indexing != 'all':
            run_django(update_suggester)

    args = parser.parse_args()
    if not args.socket and not args.port:
        args.port = 8080

    if not disconnected or disconnected == 'false':
        pre_init()

    web.run_app(
        init_app(),
        host=args.host, port=args.port, path=args.socket,
        handle_signals=True
    )
