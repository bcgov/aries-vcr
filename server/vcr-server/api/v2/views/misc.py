import logging

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import FormParser

from api.v2.feedback import email_feedback
from api.v2.models.Claim import Claim
from api.v2.models.Credential import Credential as CredentialModel
from api.v2.models.CredentialType import CredentialType
from api.v2.models.Issuer import Issuer
from api.v2.models.Topic import Topic
from api.v2.models.Name import Name
from api.v2.utils import model_counts, record_count, solr_counts, matched_solr_cred

LOGGER = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get", operation_id="api_v2_quickload", operation_description="quick load"
)
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
        "name": Name,
    }
    with connection.cursor() as cursor:
        counts = {
            mname: model_counts(model, cursor)
            for (mname, model) in count_models.items()
        }
        actual_credential_count = record_count(CredentialModel, cursor)
        actual_name_count = record_count(Name, cursor)
        actual_topic_count = record_count(Topic, cursor)

    counts["actual_credential_count"] = actual_credential_count
    counts["actual_name_count"] = actual_name_count
    counts["actual_topic_count"] = actual_topic_count
    counts["actual_item_count"] = actual_credential_count + actual_topic_count + actual_name_count
    # the returned cred_counts["total"] is actually the total number of indexed items in solr,
    # ... which includes credentials, topics and names
    cred_counts = solr_counts()
    indexes_synced = (counts["actual_item_count"] - cred_counts["total_indexed_items"]) == 0
    return JsonResponse(
        {
            "counts": counts,
            "credential_counts": cred_counts,
            "demo": settings.DEMO_SITE,
            "indexes_synced": indexes_synced,
        }
    )


@swagger_auto_schema(
    method="get", operation_id="api_v2_quickload_details", operation_description="quick load details"
)
@api_view(["GET"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
def quickload_details(request, *args, **kwargs):
    # get list of credentials from the database
    cred_rows = []
    max_rows = 1000
    with connection.cursor() as cursor:
        model_cls = CredentialModel
        query = "SELECT id, topic_id, credential_set_id, credential_id, update_timestamp FROM %s " % model_cls._meta.db_table
        #query = query + "WHERE ... "
        query = query + "ORDER BY update_timestamp "
        cursor.execute(query)
        row = cursor.fetchone()
        i = 0
        while row is not None and i < max_rows:
            cred_row = {
                "id": row[0],
                "topic_id": row[1],
                "credential_set_id": row[2],
                "credential_id": row[3],
                "update_timestamp": row[4],
            }
            # compare with what is missing in the search index
            if not matched_solr_cred(cred_row):
                cred_rows.append(cred_row)
                i = i + 1
            row = cursor.fetchone()
    return JsonResponse(cred_rows, safe=False)


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter(
            "from_name",
            openapi.IN_FORM,
            description="Sender name",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "from_email",
            openapi.IN_FORM,
            description="Sender email address",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
        ),
        openapi.Parameter(
            "comments",
            openapi.IN_FORM,
            description="Comments",
            type=openapi.TYPE_STRING,
        ),
    ],
)
@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@parser_classes((FormParser,))
def send_feedback(request, *args, **kwargs):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(",")[0]
    else:
        ip_addr = request.META.get("REMOTE_ADDR")
    from_name = request.POST.get("from_name")
    from_email = request.POST.get("from_email")
    reason = request.POST.get("reason")
    comments = request.POST.get("comments")
    email_feedback(ip_addr, from_name, from_email, reason, comments)
    return JsonResponse({"status": "ok"})
