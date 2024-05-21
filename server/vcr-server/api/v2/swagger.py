import logging

from drf_yasg import renderers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView

LOGGER = logging.getLogger(__name__)


class SwaggerSchemaView(APIView):
    """
    Utility class for rendering swagger documentation
    """

    permission_classes = (permissions.AllowAny,)
    renderer_classes = [renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer]
    schema = None

    def get(self, request):
        params = {"urlconf": "api.v2.urls"}
        if "HTTP_X_FORWARDED_HOST" in request.META:
            params["url"] = "/api"
        else:
            params["url"] = "/api/v2"
        generator = SchemaGenerator(**params)
        schema = generator.get_schema(request=request)
        return Response(schema)
