import logging

from django.apps import AppConfig

LOGGER = logging.getLogger(__name__)

class apiConfig(AppConfig):
    name = 'api'

    def ready(self):
        pass
