from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from .swagger import SwaggerSchemaView
from api_v2.views import indy, rest

router = SimpleRouter()

router.register(r"issuer", views.IssuerViewSet, "Issuer")
router.register(r"schema", views.SchemaViewSet, "Schema")
router.register(
    r"credentialtype", views.CredentialTypeViewSet, "CredentialType"
)
router.register(r"topic", views.TopicViewSet, "Topic")
router.register(r"credential", views.CredentialViewSet, "Credential")
router.register(r"address", views.AddressViewSet, "Address")
router.register(r"claim", views.ClaimViewSet, "Claim")
router.register(r"contact", views.ContactViewSet, "Contact")
router.register(r"name", views.NameViewSet, "Name")
router.register(r"person", views.PersonViewSet, "Person")


# Indy endpoints
urlpatterns = [
    url(r"^$", SwaggerSchemaView.as_view()),
    url(
        r"^indy/generate-credential-request$", indy.generate_credential_request
    ),
    url(r"^indy/store-credential$", indy.store_credential),
    url(r"^indy/register-issuer$", indy.register_issuer),
    url(r"^indy/construct-proof$", indy.construct_proof),
    url(r"^credential/(?P<id>[0-9]+)/verify$", indy.verify_credential),
] + router.urls

urlpatterns = format_suffix_patterns(urlpatterns)
