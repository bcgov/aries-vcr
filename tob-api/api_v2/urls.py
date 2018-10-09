import os

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny

from api_v2.views import misc, rest, search

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

APPLICATION_URL = os.environ.get("APPLICATION_URL")

schema_view = get_schema_view(
    openapi.Info(
        title="TheOrgBook API",
        default_version="v2",
        # description="Description goes here",
    ),
    url="{}/api/v2".format(APPLICATION_URL),
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
    url(r"^quickload$", misc.quickload)
]

swaggerPatterns = [
    url(r"^$", schema_view.with_ui("swagger", cache_timeout=None), name="api-docs"),
]

urlpatterns = format_suffix_patterns(
    router.urls + searchPatterns + miscPatterns + swaggerPatterns
)
