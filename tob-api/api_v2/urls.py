from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from .swagger import SwaggerSchemaView
from api_v2.views import misc, rest, search

router = SimpleRouter(trailing_slash=False)

router.register(r"issuer", rest.IssuerViewSet, "Issuer")
router.register(r"schema", rest.SchemaViewSet, "Schema")
router.register(
    r"credentialtype", rest.CredentialTypeViewSet, "CredentialType"
)
router.register(r"topic", rest.TopicViewSet, "Topic")
router.register(r"credential", rest.CredentialViewSet, "Credential")
router.register(r"address", rest.AddressViewSet, "Address")
router.register(r"contact", rest.ContactViewSet, "Contact")
router.register(r"name", rest.NameViewSet, "Name")
router.register(r"person", rest.PersonViewSet, "Person")
router.register(r"category", rest.CategoryViewSet, "Category")

# Search endpoints
searchPatterns = [
    url(r"^search/autocomplete$", search.NameAutocompleteView.as_view()),
    url(r"^search/topic$", search.TopicSearchView.as_view()),
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
