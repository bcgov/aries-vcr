import logging

from django.db import connection
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


def quick_counts(cursor, model_cls):
    cursor.execute(
        "SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname=%s",
        [model_cls._meta.db_table])
    row = cursor.fetchone()
    return row[0]


@api_view(["GET"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
def quickload(request, *args, **kwargs):
    count_models = {
        "address": Address,
        "claim": Claim,
        "contact": Contact,
        "credential": CredentialModel,
        "credentialtype": CredentialType,
        "issuer": Issuer,
        "name": Name,
        "person": Person,
        "schema": Schema,
        "topic": Topic,
    }
    with connection.cursor() as cursor:
        counts = {mname: quick_counts(cursor, model) for (mname, model) in count_models.items()}
    return JsonResponse(
        {
            "counts": counts,
        }
    )
