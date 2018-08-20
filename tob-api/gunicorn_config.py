"""
WSGI config for tob_api project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import asyncio
import os

# -- gunicorn settings -- #

capture_output = True
daemon = False
enable_stdio_inheritance = True
preload_app = True
workers = os.environ.setdefault('WEB_CONCURRENCY', 5)
#worker_class =
#worker_connections = 60
timeout = 60
backlog = 100
keepalive = 2
proc_name = None
errorlog = '-'
loglevel = 'debug'
pythonpath = '.'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


def on_starting(server):
    server.log.debug('Importing von-x services: pid %s', os.getpid())
    # import the shared manager instance before any processes are forked
    # this is necessary for the pipes and locks to be inherited
    from tob_anchor.boot import MANAGER
    server.service_mgr = MANAGER

def when_ready(server):
    server.log.debug('Starting von-x services: pid %s', os.getpid())
    from tob_anchor.boot import pre_init
    pre_init()

def post_fork(server, worker):
    # server.log.debug('Post-fork worker: pid %s', os.getpid())
    # this is necessary to avoid deadlocks due to the same asyncio loop ID being
    # shared by multiple processes
    asyncio.get_event_loop().close()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

def on_exit(server):
    from tob_anchor.boot import shutdown
    server.log.debug('Shutting down von-x services')
    shutdown()
