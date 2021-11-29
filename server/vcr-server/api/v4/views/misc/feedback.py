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
from api.v4.email_service import email_feedback

LOGGER = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "reason": openapi.Schema(
                type=openapi.TYPE_STRING, description="Either 'like' or 'dislike'"
            ),
            "comments": openapi.Schema(
                type=openapi.TYPE_STRING, description="Comments"
            ),
            "improvements": openapi.Schema(
                type=openapi.TYPE_STRING, description="Improvements if reason is 'dislike'"
            )
        },
    ),
)
@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@parser_classes((JSONParser,))
def send_feedback(request, *args, **kwargs):
    data = json.loads(request.body)
    reason = data.get("reason")
    comments = data.get("comments")
    improvements = data.get("improvements")
    email_feedback(reason, comments, improvements)
    return JsonResponse({"status": "ok"})
