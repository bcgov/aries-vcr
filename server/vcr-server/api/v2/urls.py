from django.urls import path
from django.conf import settings

from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.v2.views import misc, rest, search
from api.v2.utils import get_stats, clear_stats

app_name = "api_v2"

API_METADATA = settings.API_METADATA
schema_view = get_schema_view(
    openapi.Info(
        title=API_METADATA["title"],
        description=API_METADATA["description"],
        default_version="v2",
        contact=openapi.Contact(**API_METADATA["contact"]),
        license=openapi.License(**API_METADATA["license"]),
    ),
    # url="{}/api".format(settings.APPLICATION_URL),
    validators=["flex", "ssv"],
    public=True,
    permission_classes=(AllowAny,),
)

router = SimpleRouter(trailing_slash=False)

router.register(r"issuer", rest.IssuerViewSet)
router.register(r"schema", rest.SchemaViewSet)
router.register(r"credentialtype", rest.CredentialTypeViewSet)
router.register(r"credential", rest.CredentialViewSet)
router.register(r"topic", rest.TopicViewSet)
router.register(r"topic_relationship", rest.TopicRelationshipViewSet)

# Search endpoints
router.register(r"search/credential/topic",
                search.CredentialTopicSearchView, "Credential Topic Search")
router.register(r"search/credential",
                search.CredentialSearchView, "Credential Search")
router.register(r"search/autocomplete",
                search.NameAutocompleteView, "Name Autocomplete")

# Misc endpoints
miscPatterns = [
    path("feedback", misc.send_feedback),
    path("quickload", misc.quickload),
    path("status/reset", clear_stats),
    path("status", get_stats),
]

swaggerPatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=None), name="api-docs")
]

urlpatterns = format_suffix_patterns(router.urls) + miscPatterns + swaggerPatterns
