import base64
import uuid
from logging import getLogger
from time import sleep

import requests
from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v2 import utils
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
from api.v2.serializers.search import CustomTopicSerializer

logger = getLogger(__name__)


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


class TopicViewSet(ReadOnlyModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    @action(detail=True, url_path="formatted", methods=["get"])
    def retrieve_formatted(self, request, pk=None):
        item = self.get_object()
        serializer = CustomTopicSerializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ExpandedCredentialSerializer(many=True)})
    @action(detail=True, url_path="credential", methods=["get"])
    def list_credentials(self, request, pk=None):
        item = self.get_object()
        queryset = item.credentials
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ExpandedCredentialSerializer(many=True)})
    @action(detail=True, url_path="credential/active", methods=["get"])
    def list_active_credentials(self, request, pk=None):
        item = self.get_object()
        queryset = item.credentials.filter(revoked=False, inactive=False)
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ExpandedCredentialSerializer(many=True)})
    @action(detail=True, url_path="credential/historical", methods=["get"])
    def list_historical_credentials(self, request, pk=None):
        item = self.get_object()
        queryset = item.credentials.filter(Q(revoked=True) | Q(inactive=True))
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: TopicSerializer(many=False)})
    @action(
        detail=False,
        methods=["get"],
        url_path="ident/(?P<type>[^/]+)/(?P<source_id>[^/.]+)",
    )
    def retrieve_by_type(self, request, type=None, source_id=None):
        return self.retrieve(request)

    @swagger_auto_schema(responses={200: CustomTopicSerializer(many=False)})
    @action(
        detail=False,
        methods=["get"],
        url_path="ident/(?P<type>[^/]+)/(?P<source_id>[^/.]+)/formatted",
    )
    def retrieve_by_type_formatted(self, request, type=None, source_id=None):
        return self.retrieve_formatted(request)

    @swagger_auto_schema(responses={200: ExpandedCredentialSetSerializer(many=True)})
    @action(detail=True, url_path="credentialset", methods=["get"])
    def list_credential_sets(self, request, pk=None):
        item = self.get_object()
        queryset = item.credential_sets.order_by("first_effective_date").all()
        serializer = ExpandedCredentialSetSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self):
        if self.kwargs.get("pk"):
            return super(TopicViewSet, self).get_object()

        type = self.kwargs.get("type")
        source_id = self.kwargs.get("source_id")
        if not type or not source_id:
            raise Http404()

        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, type=type, source_id=source_id)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class TopicRelationshipViewSet(ReadOnlyModelViewSet):
    serializer_class = TopicRelationshipSerializer
    queryset = TopicRelationship.objects.all()

    def get_object(self):
        if self.kwargs.get("pk"):
            return super(TopicRelationshipViewSet, self).get_object()

        # I don't think the following code is used ...
        # queryset = self.filter_queryset(self.get_queryset())
        # obj = get_object_or_404(queryset, type=type, source_id=source_id)

        ## May raise a permission denied
        # self.check_object_permissions(self.request, obj)
        # return obj


class CredentialViewSet(ReadOnlyModelViewSet):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()

    @action(detail=True, url_path="formatted", methods=["get"])
    def retrieve_formatted(self, request, pk=None):
        item = self.get_object()
        serializer = ExpandedCredentialSerializer(item)
        return Response(serializer.data)

    @action(detail=True, url_path="verify", methods=["get"])
    def verify(self, request, pk=None):
        item: Credential = self.get_object()
        credential_type: CredentialType = item.credential_type

        connection_response = requests.get(
            f"{settings.AGENT_ADMIN_URL}/connections?alias={settings.AGENT_SELF_CONNECTION_ALIAS}",
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        connection_response_dict = connection_response.json()
        assert connection_response_dict["results"]

        self_connection = connection_response_dict["results"][0]

        response = requests.get(
            f"{settings.AGENT_ADMIN_URL}/credential/{item.credential_id}",
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        credential = response.json()

        proof_request = {
            "version": "1.0",
            "name": "self-verify",
            "requested_predicates": {},
            "requested_attributes": {},
        }
        request_body = {
            "connection_id": self_connection["connection_id"],
            "proof_request": proof_request,
        }
        restrictions = [{}]

        for attr in credential_type.get_tagged_attributes():
            claim_val = credential["attrs"][attr]
            restrictions[0][f"attr::{attr}::value"] = claim_val

        requested_attribute = {
            "names": [attr for attr in credential["attrs"]],
            "restrictions": restrictions,
        }
        proof_request["requested_attributes"]['self-verify-proof'] = requested_attribute

        proof_request_response = requests.post(
            f"{settings.AGENT_ADMIN_URL}/present-proof/send-request",
            json=request_body,
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        proof_request_response.raise_for_status()
        proof_request_response = proof_request_response.json()
        presentation_exchange_id = proof_request_response["presentation_exchange_id"]

        # TODO: if the agent was not started with the --auto-verify-presentation flag, verification will need to be initiated
        retries = 5
        result = None
        while retries > 0:
            sleep(5)
            retries -= 1
            presentation_state_response = requests.get(
                f"{settings.AGENT_ADMIN_URL}/present-proof/records/{presentation_exchange_id}",
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
            presentation_state = presentation_state_response.json()

            if presentation_state["state"] == "verified":
                result = {
                    "success": True,
                    "result": {
                        "presentation_request": presentation_state[
                            "presentation_request"
                        ],
                        "presentation": presentation_state["presentation"],
                    },
                }
                break

        if result is None:
            result = {"success": False, "results": "Presentation request timed out."}

        return JsonResponse(result)

    @action(detail=True, url_path="latest", methods=["get"])
    def get_latest(self, request, pk=None):
        item = self.get_object()
        latest = None
        if item.credential_set:
            latest = item.credential_set.latest_credential
        if not latest:
            latest = item
        serializer = CredentialSerializer(latest)
        return Response(serializer.data)

    def get_object(self):
        pk = self.kwargs.get("pk")
        if not pk:
            raise Http404()
        filter = {"credential_id": pk}
        try:
            filter = {"pk": int(pk)}
        except (ValueError, TypeError):
            pass

        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, **filter)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


# Add environment specific endpoints
try:
    # utils.apply_custom_methods(TopicViewSet, "views", "TopicViewSet", "includeMethods")
    utils.apply_custom_methods(
        TopicRelationshipViewSet, "views", "TopicRelationshipViewSet", "includeMethods"
    )
except:
    pass
