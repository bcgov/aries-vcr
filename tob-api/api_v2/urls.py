from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny

from api_v2.views import misc, rest, search

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TheOrgBook API",
        default_version="v2",
        description="Test description",
        #   terms_of_service="https://www.google.com/policies/terms/",
        #   contact=openapi.Contact(email="contact@snippets.local"),
        #   license=openapi.License(name="BSD License"),
    ),
    validators=["flex", "ssv"],
    public=True,
    permission_classes=(AllowAny,),
)

router = SimpleRouter(trailing_slash=False)

router.register(r"issuer", rest.IssuerViewSet)
router.register(r"schema", rest.SchemaViewSet)
router.register(r"credentialtype", rest.CredentialTypeViewSet)
router.register(r"address", rest.AddressViewSet)
router.register(r"attribute", rest.AttributeViewSet)
# router.register(r"category", rest.CategoryViewSet)
router.register(r"credential", rest.CredentialViewSet)
router.register(r"name", rest.NameViewSet)
router.register(r"topic", rest.TopicViewSet)

# Search endpoints
router.register(
    r"search/credential/topic",
    search.CredentialTopicSearchView,
    "Credential Topic Search",
)
router.register(r"search/credential", search.CredentialSearchView, "Credential Search")
searchPatterns = [url(r"^search/autocomplete$", search.NameAutocompleteView.as_view())]

# Misc endpoints
miscPatterns = [
    # Swagger documentation
    # url(r"^$", SwaggerSchemaView.as_view()),
    # Stats and cacheable info for home page
    url(r"^quickload$", misc.quickload)
]

swaggerPatterns = [
    url(r"/", schema_view.with_ui("swagger", cache_timeout=None), name="api-docs"),
    url(
        r"^swagger.json$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    # url(
    #     r"^swagger/$",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    # url(
    #     r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    # ),
]
# Indy endpoints (now handled elsewhere)
# indyPatterns = [
#    url(
#        r"^indy/generate-credential-request$", indy.generate_credential_request
#    ),
#    url(r"^indy/store-credential$", indy.store_credential),
#    url(r"^indy/register-issuer$", indy.register_issuer),
#    url(r"^indy/construct-proof$", indy.construct_proof),
#    url(r"^indy/status$", indy.status),
#    url(r"^credential/(?P<id>[0-9]+)/verify$", indy.verify_credential),
# ]

urlpatterns = format_suffix_patterns(
    swaggerPatterns + router.urls + searchPatterns + miscPatterns  # + indyPatterns
)
