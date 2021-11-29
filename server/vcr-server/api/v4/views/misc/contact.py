import logging
import json

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
from rest_framework.parsers import JSONParser
from api.v4.email_service import email_contact

LOGGER = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "from_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Sender name"
            ),
            "from_email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Sender email address"
            ),
            "reason": openapi.Schema(
                type=openapi.TYPE_STRING, description="Contact Reason"
            ),
            "comments": openapi.Schema(
                type=openapi.TYPE_STRING, description="Comments"
            ),
            "identifier": openapi.Schema(
                type=openapi.TYPE_STRING, description="Identifier code"
            ),
            "error": openapi.Schema(
                type=openapi.TYPE_STRING, description="Credential type containing the error"
            ),
        },
    ),
)
@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@parser_classes((JSONParser,))
def send_contact(request, *args, **kwargs):
    data = json.loads(request.body)
    from_name = data.get("from_name")
    from_email = data.get("from_email")
    reason = data.get("reason")
    comments = data.get("comments")
    identifier = data.get("identifier")
    error = data.get("error")
    email_contact(from_name, from_email, reason, comments, identifier=identifier, error=error)
    return JsonResponse({"status": "ok"})

