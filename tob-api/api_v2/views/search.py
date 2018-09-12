import logging

from django.conf import settings
from pysolr import Solr, SolrError

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_haystack.filters import HaystackFilter, HaystackFacetFilter
from drf_haystack.mixins import FacetMixin
from drf_haystack.viewsets import HaystackViewSet

from api_v2.models.Credential import Credential
from api_v2.serializers.search import (
    CredentialSearchSerializer, CredentialFacetSerializer,
)

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


class DefaultCredSearchFilter(HaystackFilter):
    """
    Apply default filter value(s) to credential search
    """
    @staticmethod
    def get_request_filters(request):
        filters = HaystackFilter.get_request_filters(request)
        if "revoked" not in filters:
            filters["revoked"] = "false"
        return filters


class CredentialSearchView(HaystackViewSet, FacetMixin):
    """
    Provide credential search via Solr with both faceted (/facets) and unfaceted results
    """
    index_models = [Credential]
    load_all = True
    serializer_class = CredentialSearchSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DefaultCredSearchFilter]
    facet_filter_backends = [DefaultCredSearchFilter, HaystackFacetFilter] # enable normal filtering
    facet_serializer_class = CredentialFacetSerializer
    facet_objects_serializer_class = CredentialSearchSerializer

    # FacetMixin provides /facets
