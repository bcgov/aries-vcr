import logging

from django.http import JsonResponse

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import permissions

from api_v2.models.Address import Address
from api_v2.models.Claim import Claim
from api_v2.models.Contact import Contact
from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Issuer import Issuer
from api_v2.models.Name import Name
from api_v2.models.Person import Person
from api_v2.models.Schema import Schema
from api_v2.models.Topic import Topic

LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
def quickload(request, *args, **kwargs):
    return JsonResponse(
        {
            "counts": {
                "address": Address.objects.count(),
                "claim": Claim.objects.count(),
                "contact": Contact.objects.count(),
                "credential": CredentialModel.objects.count(),
                "credentialtype": CredentialType.objects.count(),
                "issuer": Issuer.objects.count(),
                "name": Name.objects.count(),
                "person": Person.objects.count(),
                "schema": Schema.objects.count(),
                "topic": Topic.objects.count(),
            }
        }
    )
