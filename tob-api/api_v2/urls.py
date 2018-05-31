from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from .swagger import SwaggerSchemaView
from api_v2.views import indy, rest

router = SimpleRouter()

# REST endpoints
router.register(r"issuer", rest.IssuerViewSet, "Issuer")
router.register(r"schema", rest.SchemaViewSet, "Schema")
router.register(
    r"credentialtype", rest.CredentialTypeViewSet, "CredentialType"
)
router.register(r"subject", rest.SubjectViewSet, "Subject")
router.register(r"credential", rest.CredentialViewSet, "Credential")
router.register(r"address", rest.AddressViewSet, "Address")
router.register(r"claim", rest.ClaimViewSet, "Claim")
router.register(r"contact", rest.ContactViewSet, "Contact")
router.register(r"name", rest.NameViewSet, "Name")
router.register(r"person", rest.PersonViewSet, "Person")

# Indy endpoints
urlpatterns = [
    url(r"^$", SwaggerSchemaView.as_view()),
    url(
        r"^indy/generate-credential-request$", indy.generate_credential_request
    ),
    # url(r"^indy/store-claim$", indy.store_claim.as_view()),
    # url(r"^indy/construct-proof$", indy.construct_proof.as_view()),
    url(r"^indy/register-issuer$", indy.register_issuer),
] + router.urls

urlpatterns = format_suffix_patterns(urlpatterns)
