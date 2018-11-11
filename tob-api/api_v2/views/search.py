import functools
import logging
import operator

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_haystack.filters import (
    HaystackFilter,
    HaystackFacetFilter,
    HaystackAutocompleteFilter,
    HaystackOrderingFilter,
)
from drf_haystack.mixins import FacetMixin
from drf_haystack.query import BaseQueryBuilder, FilterQueryBuilder
from drf_haystack.viewsets import HaystackViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from haystack.query import RelatedSearchQuerySet
from haystack.inputs import Clean, Exact, Raw

from api_v2.models.Credential import Credential
from api_v2.serializers.search import (
    CredentialAutocompleteSerializer,
    CredentialSearchSerializer,
    CredentialFacetSerializer,
    CredentialTopicSearchSerializer,
)
from tob_api.pagination import ResultLimitPagination

LOGGER = logging.getLogger(__name__)


class Proximate(Clean):
    input_type_name = "contains"
    post_process = False # don't put AND between terms

    def prepare(self, query_obj):
        # clean input
        query_string = super(Proximate, self).prepare(query_obj)
        if query_string is not '':
            # match phrase with minimal word movements
            proximity = self.kwargs.get('proximity', 100)
            parts = query_string.split(' ')
            if len(parts) > 1:
                output = '"{}"~{}'.format(query_string, proximity)
            else:
                output = parts[0]
            if 'boost' in self.kwargs:
                output = '{}^{}'.format(output, self.kwargs['boost'])
            # increase score for any individual term
            if len(parts) > 1 and self.kwargs.get('any'):
                output = ' OR '.join([output, *parts])
        else:
            output = query_string
        return output


class AutocompleteFilterBuilder(BaseQueryBuilder):
    query_param = 'q'

    def build_name_query(self, term):
        SQ = self.view.query_object
        return SQ(name_suggest=Proximate(term)) \
               | SQ(name_precise=Proximate(term, boost=10, any=True))

    def build_query(self, **filters):
        applicable_filters = {}
        applicable_exclusions = None
        SQ = self.view.query_object
        fields = getattr(self.view.serializer_class.Meta, 'fields', [])
        exclude = getattr(self.view.serializer_class.Meta, 'exclude', [])
        search_fields = getattr(self.view.serializer_class.Meta, 'search_fields', [])
        check_fields = fields + search_fields
        for qname, qvals in filters.items():
            for qval in qvals:
                if qname == self.query_param:
                    applicable_filters[qname] = self.build_name_query(qval)
                elif qname in check_fields and qname not in exclude and qval:
                    applicable_filters[qname] = SQ(**{qname: Exact(qval)})
        applicable_filters = functools.reduce(operator.and_, applicable_filters.values())
        return applicable_filters, applicable_exclusions


class AutocompleteFilter(HaystackFilter):
    """
    Apply default filter value(s) to credential search
    """

    query_builder_class = AutocompleteFilterBuilder

    @staticmethod
    def get_request_filters(request):
        filters = HaystackFilter.get_request_filters(request)
        if "latest" not in filters:
            filters["latest"] = "true"
        if "revoked" not in filters:
            filters["revoked"] = "false"
        return filters


class NameAutocompleteView(HaystackViewSet):
    """
    Return autocomplete results for a query string
    """
    permission_classes = (permissions.AllowAny,)
    pagination_class = ResultLimitPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "q", openapi.IN_QUERY, description="Query string", type=openapi.TYPE_STRING
            ),
            #openapi.Parameter(
            #    "hl", openapi.IN_QUERY, description="Highlight search term", type=openapi.TYPE_BOOLEAN
            #),
        ])
    def list(self, *args, **kwargs):
        return super(NameAutocompleteView, self).list(*args, **kwargs)
    retrieve = None

    index_models = [Credential]
    load_all = True
    serializer_class = CredentialAutocompleteSerializer
    # enable normal filtering
    filter_backends = [
        AutocompleteFilter,
        HaystackOrderingFilter,
    ]
    ordering_fields = ('effective_date', 'revoked_date', 'score')
    ordering = ('-score')


class NameFilterBuilder(AutocompleteFilterBuilder):
    query_param = 'name'

    def build_name_query(self, term):
        SQ = self.view.query_object
        filter = super(NameFilterBuilder, self).build_name_query(term) \
               | (SQ(source_id=Exact(term)) & SQ(name=Raw('*')))
        return filter


class DefaultCredSearchFilter(AutocompleteFilter):
    """
    Apply default filter value(s) to credential search
    """

    query_builder_class = NameFilterBuilder

    @staticmethod
    def get_request_filters(request):
        filters = AutocompleteFilter.get_request_filters(request)
        if "inactive" not in filters:
            filters["inactive"] = "false"
        return filters


class CredentialSearchView(HaystackViewSet, FacetMixin):
    """
    Provide credential search via Solr with both faceted (/facets) and unfaceted results
    """

    permission_classes = (permissions.AllowAny,)

    _swagger_params = [
        openapi.Parameter(
            "name",
            openapi.IN_QUERY,
            description="Filter credentials by related name or topic source ID",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "inactive",
            openapi.IN_QUERY,
            description="Show inactive credentials",
            type=openapi.TYPE_STRING,
            enum=["", "false", "true"],
            default="false",
        ),
        openapi.Parameter(
            "latest",
            openapi.IN_QUERY,
            description="Show only latest credentials",
            type=openapi.TYPE_STRING,
            enum=["", "false", "true"],
            default="true",
        ),
        openapi.Parameter(
            "revoked",
            openapi.IN_QUERY,
            description="Show revoked credentials",
            type=openapi.TYPE_STRING,
            enum=["", "false", "true"],
            default="false",
        ),
    ]
    list = swagger_auto_schema(
        manual_parameters=_swagger_params,
    )(HaystackViewSet.list)
    retrieve = swagger_auto_schema(
        manual_parameters=_swagger_params,
    )(HaystackViewSet.retrieve)

    index_models = [Credential]
    load_all = True
    serializer_class = CredentialSearchSerializer
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
