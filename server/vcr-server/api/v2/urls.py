from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api.v2.views import misc, rest, search
from api.v2.utils import get_stats, clear_stats

router = SimpleRouter(trailing_slash=False)

router.register(r"issuer", rest.IssuerViewSet)
router.register(r"schema", rest.SchemaViewSet)
router.register(r"credentialtype", rest.CredentialTypeViewSet)
router.register(r"credential", rest.CredentialViewSet)
router.register(r"topic", rest.TopicViewSet)
router.register(r"topic_relationship", rest.TopicRelationshipViewSet)

# Search endpoints
router.register(
    r"search/credential/topic",
    search.CredentialTopicSearchView,
    "Credential Topic Search",
)
router.register(r"search/credential", search.CredentialSearchView, "Credential Search")
router.register(
    r"search/autocomplete", search.NameAutocompleteView, "Name Autocomplete"
)

# Misc endpoints
miscPatterns = [
    path("feedback", misc.send_feedback), 
    path("quickload", misc.quickload),
    path("status/reset", clear_stats),
    path("status", get_stats),
]

urlpatterns = format_suffix_patterns(router.urls) + miscPatterns
