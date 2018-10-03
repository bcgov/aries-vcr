import os
import logging

from django.conf import settings
from pysolr import Solr, SolrError

LOGGER = logging.getLogger(__name__)

class SuggestManager:
    """
    Manage interaction with Solr suggest service
    """

    def __init__(self, url: str = None):
        if not url:
            url = settings.HAYSTACK_CONNECTIONS['default']['URL']
        self.url = url
        self.handler = '/suggest'

    def query(self, query_string: str, highlight='false') -> list:
        """
        Fetch autocomplete results
        """
        rows = []
        try:
            solr = Solr(
                self.url,
                search_handler=self.handler,
                use_qt_param=False,
                results_cls=dict)
            raw_results = solr.search('', **{
                'suggest.q': query_string,
                'suggest.highlight': highlight,
            })
            if "suggest" in raw_results:
                for found in raw_results["suggest"]["autocomplete"].values():
                    rows = [
                        {"term": row["term"], "weight": row["weight"]}
                        for row in found["suggestions"]
                    ]
                    break
        except SolrError:
            LOGGER.exception("Error during Solr query:")
        return rows

    def rebuild(self):
        """
        Rebuild suggest database
        """
        try:
            if os.getenv("ENABLE_SUGGESTER_REBUILD"):
                solr = Solr(
                    self.url,
                    search_handler=self.handler)
                LOGGER.info("Rebuilding Solr suggester...")
                _results = solr.search('', **{
                    'suggest.build': 'true',
                })
            else:
                LOGGER.warn("Solr suggester rebuilding has been disabled ...")
        except SolrError:
            LOGGER.exception("Error during Solr query:")
