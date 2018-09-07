import logging

from django.conf import settings
from pysolr import Solr, SolrError

from rest_framework import permissions
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_haystack.generics import HaystackGenericAPIView

from api_v2.serializers.search import TopicSearchResultsSerializer
from api_v2.models.Topic import Topic

LOGGER = logging.getLogger(__name__)


class NameAutocompleteView(APIView):
    """
    Return autocomplete results for a query string
    """
    def get(self, request, format=None):
        query_string = request.GET.get('q', '')
        highlight = request.GET.get('hl', 'false')
        rows = []
        try:
            solr = Solr(
                settings.HAYSTACK_CONNECTIONS['default']['URL'],
                search_handler='/suggest',
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
        return Response({"result": rows})


class TopicSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [Topic]
    serializer_class = TopicSearchResultsSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
