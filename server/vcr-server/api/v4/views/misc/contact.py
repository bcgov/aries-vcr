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
            "reason",
            openapi.IN_FORM,
            description="Contact reason",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "comments",
            openapi.IN_FORM,
            description="Comments",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "identifier",
            openapi.IN_FORM,
            description="Identifier code",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "error",
            openapi.IN_FORM,
            description="Credential type containing the error",
            type=openapi.TYPE_STRING,
        ),
    ],
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

