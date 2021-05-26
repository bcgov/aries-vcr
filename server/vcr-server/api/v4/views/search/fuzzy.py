import json, logging, pysolr

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from vcr_server.haystack import config
from vcr_server.settings import HAYSTACK_CONNECTIONS

from api.v4.serializers.search.fuzzy import SearchSerializer

LOGGER = logging.getLogger(__name__)

# Create a solr client instance.
solr_url = ''
if 'URL' in HAYSTACK_CONNECTIONS['default']:
    solr_url = HAYSTACK_CONNECTIONS['default']['URL']
solr_client = pysolr.Solr(solr_url, always_commit=True)

swagger_params = [
    # Put additional parameters here
    openapi.Parameter(
        "q",
        openapi.IN_QUERY,
        description="Enter an Apache Leucene query that will return matching Solr indexes",
        type=openapi.TYPE_STRING,
    )
]


class SearchView(ViewSet):
    """
    ViewSet that will forward an Apache Leucene query directly to Solr
    """
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(manual_parameters=swagger_params)
    def list(self, request):
        try:
            query_params = request.query_params
            q = query_params.get('q', None)
            if (not q):
                return Response("Query parameter \'q\' is required", status.HTTP_400_BAD_REQUEST)
            results = solr_client.search(f'topic_name_suggest:{q}')
            return Response(SearchSerializer(results, many=True).data)
        except Exception as e:
            LOGGER.error(e)
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
