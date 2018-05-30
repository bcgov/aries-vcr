from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from .swagger import SwaggerSchemaView
from api_v2.views import indy, rest

router = SimpleRouter()

# REST endpoints
router.register(r"issuer", rest.IssuerViewSet, "Issuer")
router.register(r"schema", rest.SchemaViewSet, "Schema")
router.register(
    r"credentialtype", rest.CredentialTypeViewSet, "CredentialType"
)

# Indy endpoints
urlpatterns = [
    url(r"^$", SwaggerSchemaView.as_view()),
    # url(r"^indy/generate-claim-request$", indy.bcovrinGenerateClaimRequest.as_view()),
    # url(r"^indy/store-claim$", indy.bcovrinStoreClaim.as_view()),
    # url(r"^indy/construct-proof$", indy.bcovrinConstructProof.as_view()),
    url(r"^indy/register-issuer$", indy.register_issuer.as_view()),
] + router.urls


urlpatterns = format_suffix_patterns(urlpatterns)
