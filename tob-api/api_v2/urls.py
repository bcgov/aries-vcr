from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .swagger import SwaggerSchemaView
from api_v2.views import indy


urlpatterns = [
    url(r"^$", SwaggerSchemaView.as_view()),
    # url(r"^indy/generate-claim-request$", indy.bcovrinGenerateClaimRequest.as_view()),
    # url(r"^indy/store-claim$", indy.bcovrinStoreClaim.as_view()),
    # url(r"^indy/construct-proof$", indy.bcovrinConstructProof.as_view()),
    url(r"^indy/register-issuer$", indy.register_issuer.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
