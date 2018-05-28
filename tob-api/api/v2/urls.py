from django.conf.urls import url
from django.views.generic import RedirectView

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger import renderers


from api.v2.views import indy


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer]
    _ignore_model_permissions = True
    exclude_from_schema = True

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        return Response(schema)


urlpatterns = [
    # Swagger documentation
    url(r"^$", SwaggerSchemaView.as_view()),
    url(r"^indy/generate-claim-request$",
        indy.bcovrinGenerateClaimRequest.as_view()),

    url(r"^bcovrin/register-issuer$", indy.bcovrinRegisterIssuer.as_view()),

    url(r"^indy/store-claim$", indy.bcovrinStoreClaim.as_view()),
    url(r"^indy/construct-proof$", indy.bcovrinConstructProof.as_view()),
    url(r"^indy/register-issuer$", indy.bcovrinRegisterIssuer.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
