import pysolr
import json

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from vcr_server.haystack import config

from api.v4.serializers.search.fuzzy import SearchSerializer

# Create a solr client instance.
solr_config = config()
solr_url = solr_config['URL'] if solr_config else ''
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
            return Response(f'There was a problem with the request', status.HTTP_500_INTERNAL_SERVER_ERROR)
