import logging

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_haystack.filters import HaystackFilter, HaystackFacetFilter, HaystackOrderingFilter
from drf_haystack.mixins import FacetMixin
from drf_haystack.query import FilterQueryBuilder
from drf_haystack.viewsets import HaystackViewSet
from haystack.query import RelatedSearchQuerySet

from api_v2.models.Credential import Credential
from api_v2.serializers.search import (
    CredentialSearchSerializer,
    CredentialFacetSerializer,
    CredentialTopicSearchSerializer,
)
from api_v2.suggest import SuggestManager

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

LOGGER = logging.getLogger(__name__)


class NameAutocompleteView(APIView):
    """
    Return autocomplete results for a query string
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "q", openapi.IN_QUERY, description="Query string", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "hl", openapi.IN_QUERY, description="Highlight search term", type=openapi.TYPE_BOOLEAN
            ),
        ]
    )
    def get(self, request, format=None):
        query_string = request.GET.get("q", "")
        highlight = request.GET.get("hl", "false")
        rows = SuggestManager().query(query_string, highlight)
        return Response({"result": rows})


class CustomFilterBuilder(FilterQueryBuilder):
    @staticmethod
    def tokenize(stream, separator):
        """
        Do not tokenize filter input - pass through to Solr to tokenize
        The default implementation splits by ',' and joins with 'OR'
        """
        for value in stream:
            yield value

    def build_query(self, **filters):
        """
        Custom handling for name filter
        Search by name and name_precise (using __exact to pass through the query)
        allowing results to be ordered more naturally
        """
        name_filter = None
        SQ = self.view.query_object
        if 'name' in filters:
            name = filters.pop("name")
            if name is not None and len(name):
                name_filter = SQ(('name__exact', name)) | SQ(('name_precise__exact', name))
        applicable_filters, applicable_exclusions = super(CustomFilterBuilder, self).build_query(**filters)
        if name_filter:
            applicable_filters = (name_filter & applicable_filters) if applicable_filters else name_filter
        return applicable_filters, applicable_exclusions


class DefaultCredSearchFilter(HaystackFilter):
    """
    Apply default filter value(s) to credential search
    """

    query_builder_class = CustomFilterBuilder

    @staticmethod
    def get_request_filters(request):
        filters = HaystackFilter.get_request_filters(request)
        if "inactive" not in filters:
            filters["inactive"] = "false"
        if "latest" not in filters:
            filters["latest"] = "true"
        if "revoked" not in filters:
            filters["revoked"] = "false"
        return filters


class CredentialSearchView(HaystackViewSet, FacetMixin):
    """
    Provide credential search via Solr with both faceted (/facets) and unfaceted results
    """

    list = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "name", openapi.IN_QUERY, description="Filter credentials by related name", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "inactive", openapi.IN_QUERY, description="Filter inactive credentials ('true'/'false'/'' for all)", type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                "revoked", openapi.IN_QUERY, description="Filter revoked credentials ('true'/'false'/'' for all)", type=openapi.TYPE_BOOLEAN
            ),
        ]
    )(HaystackViewSet.list)
    retrieve = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "name", openapi.IN_QUERY, description="Filter credentials by related name", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "inactive", openapi.IN_QUERY, description="Filter inactive credentials ('true'/'false'/'' for all)", type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                "revoked", openapi.IN_QUERY, description="Filter revoked credentials ('true'/'false'/'' for all)", type=openapi.TYPE_BOOLEAN
            ),
        ]
    )(HaystackViewSet.retrieve)

    index_models = [Credential]
    load_all = True
    serializer_class = CredentialSearchSerializer
    permission_classes = (permissions.AllowAny,)
    # enable normal filtering
    filter_backends = [
        DefaultCredSearchFilter,
        HaystackOrderingFilter,
    ]
    facet_filter_backends = [
        DefaultCredSearchFilter,
        HaystackOrderingFilter,
        HaystackFacetFilter,
    ]
    facet_serializer_class = CredentialFacetSerializer
    facet_objects_serializer_class = CredentialSearchSerializer
    ordering_fields = ('effective_date', 'revoked_date', 'score')
    ordering = ('-score')

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
