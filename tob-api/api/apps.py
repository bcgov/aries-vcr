import logging

from django.apps import AppConfig
#from tob_anchor.boot import MANAGER

from . import eventloop

LOGGER = logging.getLogger(__name__)

class apiConfig(AppConfig):
    name = 'api'

    def ready(self):
        pass

        # eventloop.do(MANAGER.get_client().sync())
        # LOGGER.info("synced worker")
