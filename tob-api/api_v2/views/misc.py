import logging

from django.db import connection
from django.http import JsonResponse

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import permissions

from api_v2.models.Claim import Claim
from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Issuer import Issuer
from api_v2.models.Topic import Topic
from api_v2.utils import model_counts

LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
def quickload(request, *args, **kwargs):
    count_models = {
        "claim": Claim,
        "credential": CredentialModel,
        "credentialtype": CredentialType,
        "issuer": Issuer,
        "topic": Topic,
    }
    with connection.cursor() as cursor:
        counts = {mname: model_counts(model, cursor) for (mname, model) in count_models.items()}
    return JsonResponse(
        {
            "counts": counts,
        }
    )
