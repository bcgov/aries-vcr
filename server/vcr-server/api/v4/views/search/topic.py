from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_haystack.mixins import FacetMixin
from drf_haystack.filters import HaystackOrderingFilter

from api.v2.search.filters import CustomFacetFilter

from api.v2.models.Topic import Topic

from api.v3.views.search import (
    AriesHaystackViewSet,
    credential_search_swagger_params as swagger_params,
)

from api.v4.search.filters.topic import (
    TopicCategoryFilter,
    TopicExactFilter,
    TopicQueryFilter,
    TopicStatusFilter,
    filter_display_names
)

from api.v4.serializers.search.topic import SearchSerializer, FacetSerializer

_deprecated_params = ('name', 'topic_id', 'credential_type_id',
                      'topic_credential_type_id')
_swagger_params = [
    # Put additional parameters here
    openapi.Parameter(
        "q",
        openapi.IN_QUERY,
        description="Filter topics by related name, address or Topic Source ID",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "ordering",
        openapi.IN_QUERY,
        description="Which field to use when ordering the results ('effective_date', 'revoked_date', 'score').",
        type=openapi.TYPE_STRING,
        default="-score",
    ),
] + list(filter(lambda param: param.name not in _deprecated_params, swagger_params)) + [
    openapi.Parameter(
        "type_id",
        openapi.IN_QUERY,
        description="Filter by Credential Type ID of the Topic",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "credential_type_id",
        openapi.IN_QUERY,
        description="Filter by Credential Type ID of any credentials owned by the Topic",
        type=openapi.TYPE_STRING,
    ),
]


class SearchView(AriesHaystackViewSet, FacetMixin):
    """
    Provide Topic search via Solr with both faceted (/facets) and unfaceted results
    """

    permission_classes = (permissions.AllowAny,)

    index_models = [Topic]
    serializer_class = SearchSerializer
    facet_serializer_class = FacetSerializer
    facet_objects_serializer_class = SearchSerializer
    ordering_fields = ("effective_date", "revoked_date", "score")
    ordering = "-score"

    # Backends need to be added in the order of filter operations to be applied
    filter_backends = [
        TopicQueryFilter,
        TopicCategoryFilter,
        TopicExactFilter,
        TopicStatusFilter,
        HaystackOrderingFilter,
    ]

    # Backends need to be added in the order of filter operations to be applied
    facet_filter_backends = [
        TopicQueryFilter,
        TopicExactFilter,
        TopicStatusFilter,
        CustomFacetFilter,
    ]

    @swagger_auto_schema(manual_parameters=_swagger_params)
    def list(self, *args, **kwargs):
        return super(SearchView, self).list(*args, **kwargs)

    # FacetMixin provides /facets
    @action(detail=False, methods=["get"], url_path="facets")
    def facets(self, request):
        queryset = self.get_queryset()
        facet_queryset = self.filter_facet_queryset(queryset)
        result_queryset = self.filter_queryset(queryset)

        narrow_dict = {}
        for key in filter_display_names:
            # We dont want to restrict the facets by status
            if key in ('inactive', 'revoked'):
                continue
            for value in request.query_params.getlist(key):
                if value:
                    narrow_dict['topic_'
                                + key] = queryset.query.clean(value)

        for query_param in request.query_params:
            # For category query parameters of the form category:<category_name>=<category_value>
            if ':' not in query_param:
                continue
            key, category = query_param.split(":", 1)
            if not key or not category or (key not in filter_display_names):
                continue
            for value in request.query_params.getlist(query_param):
                if value:
                    narrow_dict['topic_'
                                + key] = queryset.query.clean('{}::{}'.format(category, value))

        for key, value in narrow_dict.items():
            facet_queryset = facet_queryset.narrow('{}:{}'.format(key, value))

        serializer = self.get_facet_serializer(
            facet_queryset.facet_counts(), objects=result_queryset, many=False
        )

        return Response(serializer.data)
