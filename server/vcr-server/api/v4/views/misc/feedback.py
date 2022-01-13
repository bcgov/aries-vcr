import logging
import json

from django.http import JsonResponse, HttpResponse
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
from api.v2.models import Feedback

import datetime
from django.utils import timezone

LOGGER = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="return email address"
            ),
            "comments": openapi.Schema(
                type=openapi.TYPE_STRING, description="Comments"
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
    email = data.get("email")
    comments = data.get("comments")
    email_feedback(email, comments)
    return JsonResponse({"status": "ok"})


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "like": openapi.Schema(
                type=openapi.TYPE_BOOLEAN, description="Either 'like' or 'dislike'"
            )
        },
    ),
)
@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@parser_classes((JSONParser,))
def send_like(request, *args, **kwargs):
    response = HttpResponse()
    data = json.loads(request.body)
    like = data.get("like")
    if not like:
        return HttpResponse("Bad Input: Please specify either true or false in the 'like' paramater", status=400)
    ip = request.META.get('REMOTE_ADDR')

    for q in Feedback.Feedback.objects.filter(ip=ip):
        if q.date and timezone.now() - q.date < datetime.timedelta(days=1):
            return HttpResponse("You have exceed the request limit for today", status=401)
    feed = Feedback.Feedback.objects.create()
    feed.like = like
    feed.ip = ip
    feed.save()
    
    return HttpResponse(status=200)