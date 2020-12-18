import base64
import uuid
import os
from logging import getLogger
from time import sleep

from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.views import APIView

from api.v2.utils import apply_custom_methods, call_agent_with_retry
from api.v2.models.Credential import Credential
from api.v2.models.CredentialType import CredentialType
from api.v2.models.Issuer import Issuer
from api.v2.models.Schema import Schema
from api.v2.models.Topic import Topic
from api.v2.models.TopicRelationship import TopicRelationship

from api.v2.serializers.rest import (
    CredentialSerializer,
    CredentialTypeSerializer,
    ExpandedCredentialSerializer,
    ExpandedCredentialSetSerializer,
    IssuerSerializer,
    SchemaSerializer,
    TopicRelationshipSerializer,
    TopicSerializer,
)

from .viewsets import RetriveOnlyModelViewSet
from ..mixins import MultipleFieldLookupMixin

from api.v2.serializers.search import CustomTopicSerializer

logger = getLogger(__name__)

TRACE_PROOF_EVENTS = os.getenv("TRACE_PROOF_EVENTS", "false").lower() == "true"


class IssuerViewSet(ReadOnlyModelViewSet):
    serializer_class = IssuerSerializer
    queryset = Issuer.objects.all()

    @swagger_auto_schema(responses={200: CredentialTypeSerializer(many=True)})
    @action(detail=True, url_path="credentialtype", methods=["get"])
    def list_credential_types(self, request, pk=None):
        item = self.get_object()
        queryset = item.credential_types
        serializer = CredentialTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(method="get")
    @action(detail=True, url_path="logo", methods=["get"])
    def fetch_logo(self, request, pk=None):
        issuer = get_object_or_404(self.queryset, pk=pk)
        logo = None
        if issuer.logo_b64:
            logo = base64.b64decode(issuer.logo_b64)
        if not logo:
            raise Http404()
        # FIXME - need to store the logo mime type
        return HttpResponse(logo, content_type="image/jpg")


class SchemaViewSet(ReadOnlyModelViewSet):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("id", "name", "version", "origin_did")


class CredentialTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = CredentialTypeSerializer
    queryset = CredentialType.objects.all()

    @action(detail=True, url_path="logo", methods=["get"])
    def fetch_logo(self, request, pk=None):
        cred_type = get_object_or_404(self.queryset, pk=pk)
        logo = None
        if cred_type.logo_b64:
            logo = base64.b64decode(cred_type.logo_b64)
        elif cred_type.issuer and cred_type.issuer.logo_b64:
            logo = base64.b64decode(cred_type.issuer.logo_b64)
        if not logo:
            raise Http404()
        # FIXME - need to store the logo mime type
        return HttpResponse(logo, content_type="image/jpg")

    @action(detail=True, url_path="language", methods=["get"])
    def fetch_language(self, request, pk=None):
        cred_type = get_object_or_404(self.queryset, pk=pk)
        lang = {
            "category_labels": cred_type.category_labels,
            "claim_descriptions": cred_type.claim_descriptions,
            "claim_labels": cred_type.claim_labels,
        }
        return Response(lang)


class TopicView(APIView):
    queryset = Topic.objects.all()

    def get(self, request, type, source_id):
        topic = get_object_or_404(self.queryset, type=type, source_id=source_id)
        serializer = TopicSerializer(topic, many=False)
        return Response(serializer.data)


class InvalidTopicAttributeQuery(APIException):
    status_code = 400
    default_detail = 'Attribute query must be in the format "attribute_name::value".'
    default_code = 'topic_attribute_query_error'


class TopicAttributeView(APIView):
    queryset = Topic.objects.all()

    def get(self, request, attribute_query):
        attributes_query = attribute_query.split('::')
        if len(attributes_query) != 2:
            raise InvalidTopicAttributeQuery()

        topics = self.queryset.filter(
            credentials__attributes__type=attributes_query[0],
            credentials__attributes__value=attributes_query[1],
        )[:200]
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class CredentialViewSet(RetriveOnlyModelViewSet):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()
    lookup_field = "credential_id"

    @action(detail=True, url_path="verify", methods=["get"])
    def verify(self, request, credential_id):
        item: Credential = self.get_object()
        credential_type: CredentialType = item.credential_type

        connection_response = call_agent_with_retry(
            f"{settings.AGENT_ADMIN_URL}/connections?alias={settings.AGENT_SELF_CONNECTION_ALIAS}",
            post_method=False,
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        connection_response_dict = connection_response.json()
        assert connection_response_dict["results"]

        self_connection = connection_response_dict["results"][0]

        response = call_agent_with_retry(
            f"{settings.AGENT_ADMIN_URL}/credential/{item.credential_id}",
            post_method=False,
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        response.raise_for_status()
        credential = response.json()

        # use the credential_id in the name of the proof request - this allows the
        # prover to short-circuit the anoncreds function to fetch the credential directly
        proof_request = {
            "version": "1.0",
            "name": "cred_id::" + item.credential_id,
            "requested_predicates": {},
            "requested_attributes": {},
        }
        request_body = {
            "connection_id": self_connection["connection_id"],
            "proof_request": proof_request,
        }
        if TRACE_PROOF_EVENTS:
            request_body["trace"] = TRACE_PROOF_EVENTS
        restrictions = [{}]
        restrictions[0]["cred_def_id"] = credential_type.credential_def_id

        for attr in credential_type.get_tagged_attributes():
            claim_val = credential["attrs"][attr]
            restrictions[0][f"attr::{attr}::value"] = claim_val

        requested_attribute = {
            "names": [attr for attr in credential["attrs"]],
            "restrictions": restrictions,
        }
        proof_request["requested_attributes"]["self-verify-proof"] = requested_attribute

        proof_request_response = call_agent_with_retry(
            f"{settings.AGENT_ADMIN_URL}/present-proof/send-request",
            post_method=True,
            payload=request_body,
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        proof_request_response.raise_for_status()
        proof_request_response = proof_request_response.json()
        presentation_exchange_id = proof_request_response["presentation_exchange_id"]

        result = {
            "success": True,
            "presentation_exchange_id": presentation_exchange_id,
            "presentation_exchange": proof_request_response,
        }

        # TODO: if the agent was not started with the --auto-verify-presentation flag, verification will need to be initiated

        return JsonResponse(result)

    @action(detail=True, url_path="verify/(?P<presentation_exchange_id>[^/.]+)", methods=["get"])
    def post_verify(self, request, credential_id, presentation_exchange_id):
        result = None
        presentation_state_response = call_agent_with_retry(
            f"{settings.AGENT_ADMIN_URL}/present-proof/records/{presentation_exchange_id}",
            post_method=False,
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        presentation_state = presentation_state_response.json()

        if presentation_state["state"] == "verified":
            result = {
                "success": True,
                "state": presentation_state["state"],
                "result": {
                    "presentation_request": presentation_state[
                        "presentation_request"
                    ],
                    "presentation": presentation_state["presentation"],
                },
            }
        else:
            result = {
                "success": False,
                "state": presentation_state["state"],
                "result": {
                    "presentation_request": presentation_state[
                        "presentation_request"
                    ],
                },
            }
            if "presentation" in presentation_state:
                result["result"]["presentaiton"] = presentation_state["presentation"]

        if result is None:
            result = {"success": False,
                      "results": "Presentation request response not available."}

        return JsonResponse(result)

    @action(detail=True, url_path="latest", methods=["get"])
    def get_latest(self, request, credential_id=None):
        item = self.get_object()
        latest = None
        if item.credential_set:
            latest = item.credential_set.latest_credential
        if not latest:
            latest = item
        serializer = CredentialSerializer(latest)
        return Response(serializer.data)

    def get_object(self):
        credential_id = self.kwargs.get("credential_id")
        if not credential_id:
            raise Http404()

        filter = {"credential_id": credential_id}
        # if the input parameter is a pure int, treat as an internal database pk
        # (for reverse compatibility with the old "v2" api)
        try:
            filter = {"pk": int(credential_id)}
        except (ValueError, TypeError):
            pass

        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, **filter)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
