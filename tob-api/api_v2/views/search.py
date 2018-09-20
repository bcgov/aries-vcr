import logging

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_haystack.filters import HaystackFilter, HaystackFacetFilter
from drf_haystack.mixins import FacetMixin
from drf_haystack.viewsets import HaystackViewSet
from haystack.query import RelatedSearchQuerySet

from api_v2.models.Credential import Credential
from api_v2.serializers.search import (
    CredentialSearchSerializer, CredentialFacetSerializer,
    CredentialTopicSearchSerializer,
)
from api_v2.suggest import SuggestManager

LOGGER = logging.getLogger(__name__)


class NameAutocompleteView(APIView):
    """
    Return autocomplete results for a query string
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        query_string = request.GET.get('q', '')
        highlight = request.GET.get('hl', 'false')
        rows = SuggestManager().query(query_string, highlight)
        return Response({"result": rows})


class DefaultCredSearchFilter(HaystackFilter):
    """
    Apply default filter value(s) to credential search
    """
    @staticmethod
    def get_request_filters(request):
        filters = HaystackFilter.get_request_filters(request)
        if "inactive" not in filters:
            filters["inactive"] = "false"
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


class TopicSearchQuerySet(RelatedSearchQuerySet):
    """
    Optimize queries when fetching topic-oriented credential search results
    """
    def __init__(self, *args, **kwargs):
        super(TopicSearchQuerySet, self).__init__(*args, **kwargs)
        self._load_all_querysets[Credential] = self.topic_queryset()

    def topic_queryset(self):
        return Credential.objects.select_related(
            "credential_type",
            "credential_type__issuer",
            "credential_type__schema",
            "topic",
        ).all()


class CredentialTopicSearchView(CredentialSearchView):
    object_class = TopicSearchQuerySet
    serializer_class = CredentialTopicSearchSerializer
    facet_objects_serializer_class = CredentialTopicSearchSerializer
