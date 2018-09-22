from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from .swagger import SwaggerSchemaView
from api_v2.views import misc, rest, search

router = SimpleRouter(trailing_slash=False)

router.register(r"issuer", rest.IssuerViewSet)
router.register(r"schema", rest.SchemaViewSet)
router.register(r"credentialtype", rest.CredentialTypeViewSet)
router.register(r"address", rest.AddressViewSet)
router.register(r"attribute", rest.AttributeViewSet)
#router.register(r"category", rest.CategoryViewSet)
router.register(r"credential", rest.CredentialViewSet)
router.register(r"name", rest.NameViewSet)
router.register(r"topic", rest.TopicViewSet)

# Search endpoints
router.register(
    r"search/credential/topic", search.CredentialTopicSearchView, "Credential Topic Search")
router.register(
    r"search/credential", search.CredentialSearchView, "Credential Search")
searchPatterns = [
    url(r"^search/autocomplete$", search.NameAutocompleteView.as_view()),
]

# Misc endpoints
miscPatterns = [
    # Swagger documentation
    url(r'^$', SwaggerSchemaView.as_view()),
    # Stats and cacheable info for home page
    url(r"^quickload$", misc.quickload),
]

# Indy endpoints (now handled elsewhere)
#indyPatterns = [
#    url(
#        r"^indy/generate-credential-request$", indy.generate_credential_request
#    ),
#    url(r"^indy/store-credential$", indy.store_credential),
#    url(r"^indy/register-issuer$", indy.register_issuer),
#    url(r"^indy/construct-proof$", indy.construct_proof),
#    url(r"^indy/status$", indy.status),
#    url(r"^credential/(?P<id>[0-9]+)/verify$", indy.verify_credential),
#]

urlpatterns = format_suffix_patterns(
    router.urls + searchPatterns + miscPatterns # + indyPatterns
)
