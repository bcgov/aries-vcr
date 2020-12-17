from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_haystack.filters import HaystackOrderingFilter

from api.v2.search.filters import (
    CategoryFilter,
    CustomFacetFilter,
    ExactFilter,
    StatusFilter,
)

from api.v4.search.filters.credential import CredQueryFilter

from api.v2.views.search import CredentialSearchView

from api.v3.views.search import (
    credential_search_swagger_params as swagger_params,
)

_deprecated_params = ('name',)
_swagger_params = [
    # Put additional parameters here
    openapi.Parameter(
        "q",
        openapi.IN_QUERY,
        description="Filter credentials by related name, address or Topic Source ID",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "ordering",
        openapi.IN_QUERY,
        description="Which field to use when ordering the results ('effective_date', 'revoked_date', 'score').",
        type=openapi.TYPE_STRING,
        default="-score",
    ),
] + list(filter(lambda param: param.name not in _deprecated_params, swagger_params))


class SearchView(CredentialSearchView):
    """
    Provide Credential search via Solr with both faceted (/facets) and unfaceted results
    """

    @swagger_auto_schema(manual_parameters=_swagger_params)
    def list(self, *args, **kwargs):
        return super(SearchView, self).list(*args, **kwargs)

    filter_backends = [
        CategoryFilter,
        CredQueryFilter,
        ExactFilter,
        StatusFilter,
        HaystackOrderingFilter,
    ]

    facet_filter_backends = [
        ExactFilter,
        CredQueryFilter,
        StatusFilter,
        CustomFacetFilter,
    ]