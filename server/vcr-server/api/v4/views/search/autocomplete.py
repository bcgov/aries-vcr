import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_haystack.serializers import HaystackSerializer

from api.v3.views.search import (
    AggregateAutocompleteView,
    aggregate_autocomplete_swagger_params as swagger_params,
)
from api.v3.serializers.search import (
    AddressAutocompleteSerializer,
    NameAutocompleteSerializer,
    TopicAutocompleteSerializer,
)
from api.v3.search_filters import (
    AutocompleteFilter,
    StatusFilter as AutocompleteStatusFilter,
)
from api.v4.search.filters.topic import (
    TopicCategoryFilter as AutocompleteCategoryFilter,
    TopicExactFilter as AutocompleteExactFilter,
)
from api.v3.indexes import (
    Address as AddressIndex,
    Name as NameIndex,
    Topic as TopicIndex,
)

LOGGER = logging.getLogger(__name__)


class AggregateAutocompleteSerializer(HaystackSerializer):
    class Meta:
        serializers = {
            AddressIndex: AddressAutocompleteSerializer,
            NameIndex: NameAutocompleteSerializer,
            TopicIndex: TopicAutocompleteSerializer,
        }

        filter_fields_map = {
            "category": ("topic_category",),
            "issuer_id": ("topic_issuer_id"),
            "type_id": ("topic_type_id"),
            "credential_type_id": ("topic_credential_type_id"),
            "inactive": (
                "address_credential_inactive",
                "name_credential_inactive",
                "topic_all_credentials_inactive",
            ),
            "revoked": (
                "address_credential_revoked",
                "name_credential_revoked",
                "topic_all_credentials_revoked",
            ),
        }


_swagger_params = [
    openapi.Parameter(
        "category",
        openapi.IN_QUERY,
        description="Filter by Credential Category. The category name and value should be joined by '::'",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "type_id",
        openapi.IN_QUERY,
        description="Filter by Credential Type ID of the Topic",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "issuer_id",
        openapi.IN_QUERY,
        description="Filter by Issuer ID of the Topic",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "credential_type_id",
        openapi.IN_QUERY,
        description="Filter by Credential Type ID of any credentials owned by the Topic",
        type=openapi.TYPE_STRING,
    ),
    # Put additional parameters here
] + list(swagger_params)


class SearchView(AggregateAutocompleteView):
    """
    Return autocomplete results for a query string
    """

    @swagger_auto_schema(
        manual_parameters=_swagger_params,
        responses={200: AggregateAutocompleteSerializer(many=True)},
    )
    def list(self, *args, **kwargs):
        return super(SearchView, self).list(*args, **kwargs)

    filter_backends = (
        AutocompleteFilter,
        AutocompleteStatusFilter,
        AutocompleteCategoryFilter,
        AutocompleteExactFilter,
    )
