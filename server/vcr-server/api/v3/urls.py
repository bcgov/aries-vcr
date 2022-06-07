from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api.v3.views import rest, search
from api.v2.swagger import HttpsSchemaGenerator

app_name = "api_v3"

API_METADATA = settings.API_METADATA
schema_view = get_schema_view(
    openapi.Info(
        title=API_METADATA["title"],
        default_version="v3",
        description=API_METADATA["description"],
        terms_of_service=API_METADATA["terms"]["url"],
        contact=openapi.Contact(**API_METADATA["contact"]),
        license=openapi.License(**API_METADATA["license"]),
    ),
    # url="{}/api".format(settings.APPLICATION_URL),
    validators=["flex", "ssv"],
    generator_class=HttpsSchemaGenerator,
    public=True,
    permission_classes=(AllowAny,),
)

router = SimpleRouter(trailing_slash=False)

router.register(r"issuer", rest.IssuerViewSet, "Credential Issuer")
router.register(r"schema", rest.SchemaViewSet, "Credential Schema")
router.register(r"credentialtype", rest.CredentialTypeViewSet, "Credential Type")
router.register(r"credential", rest.CredentialViewSet, "Credential")

api_views = [
    path("search/topic/attribute/<attribute_query>", rest.TopicAttributeView.as_view()),
    path("topic/<type>/<source_id>", rest.TopicView.as_view()),
]

# Search endpoints
router.register(r"search/autocomplete",
                search.AggregateAutocompleteView, "Aggregate Autocomplete")
router.register(r"search/credential",
                search.CredentialSearchView, "Credential Search")
# DEPRECATED:
router.register(r"search/topic",
                search.CredentialTopicSearchView, "Credential Topic Search")

swaggerPatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=None), name="api-docs")
]

urlpatterns = format_suffix_patterns(router.urls) + api_views + swaggerPatterns
