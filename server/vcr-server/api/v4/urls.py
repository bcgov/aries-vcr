from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api.v4.views.search import (
    topic as search_topic,
    credential as search_credential,
    fuzzy as search_fuzzy,
    # DEPRECATED: this should not be used in new code and will be removed imminently
    autocomplete as search_autocomplete,
)
from api.v4.views.rest import credential_type, issuer, topic, schemas
from api.v4.views.misc.contact import send_contact
from api.v4.views.misc.feedback import send_feedback

app_name = "api_v4"

API_METADATA = settings.API_METADATA
schema_view = get_schema_view(
    openapi.Info(
        title=API_METADATA["title"],
        default_version="v4",
        description=API_METADATA["description"],
        terms_of_service=API_METADATA["terms"]["url"],
        contact=openapi.Contact(**API_METADATA["contact"]),
        license=openapi.License(**API_METADATA["license"]),
    ),
    validators=["flex", "ssv"],
    public=True,
    permission_classes=(AllowAny,),
)

router = SimpleRouter(trailing_slash=False)

router.register(r"credential-type",
                credential_type.RestView, "Credential Type")
router.register(r"issuer", issuer.RestView, "Issuer")
router.register(r"schemas", schemas.RestView)
router.register(r"topic", topic.RestView)
router.register(r"search/credential",
                search_credential.SearchView, "Credential Search")
router.register(r"search/topic", search_topic.SearchView, "Topic Search")
router.register(r"search/fuzzy", search_fuzzy.SearchView, "Fuzzy Search")
# DEPRECATED: this should not be used in new code and will be removed imminently
router.register(r"search/autocomplete",
                search_autocomplete.SearchView, "Aggregate Autocomplete")

# Misc endpoints
miscPatterns = [
    path("contact", send_contact),
    path("feedback", send_feedback),
]

swaggerPatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=None), name="api-docs")
]

urlpatterns = format_suffix_patterns(
    router.urls) + miscPatterns + swaggerPatterns
