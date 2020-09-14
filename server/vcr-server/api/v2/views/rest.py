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
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

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
from api.v2.serializers.search import CustomTopicSerializer

logger = getLogger(__name__)

TRACE_PROOF_EVENTS = os.getenv("TRACE_PROOF_EVENTS", "false").lower() == "true"

# max attempts to wait for a proof response
PROOF_RETRY_MAX_ATTEMPTS  = int(os.getenv("PROOF_RETRY_MAX_ATTEMPTS", "7"))
# initial delay in msec between checks for a proof response
PROOF_RETRY_INITIAL_DELAY = float(os.getenv("PROOF_RETRY_INITIAL_DELAY", "500"))
# backoff factor (2 = double the delay with each proof response check)
PROOF_RETRY_DELAY_BACKOFF = float(os.getenv("PROOF_RETRY_DELAY_BACKOFF", "2"))


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

        credential_sets = (
            item.credential_sets
            # .select_related("credential_type", "topic")
            .prefetch_related(
                # "credentials__addresses",
                "credentials__related_topics",
                "credentials__credential_type",
                "credentials__topic",
            )
            .order_by("first_effective_date")
            .all()
        )

        data = [
            {
                "id": credential_set.id,
                "create_timestamp": credential_set.create_timestamp.isoformat()
                if credential_set.create_timestamp is not None
                else None,
                "update_timestamp": credential_set.update_timestamp.isoformat()
                if credential_set.update_timestamp is not None
                else None,
                "latest_credential_id": credential_set.latest_credential_id,
                "topic_id": credential_set.topic_id,
                "first_effective_date": credential_set.first_effective_date.isoformat()
                if credential_set.first_effective_date is not None
                else None,
                "last_effective_date": credential_set.last_effective_date.isoformat()
                if credential_set.last_effective_date is not None
                else None,
                "credentials": [
                    {
                        "id": credential.id,
                        "create_timestamp": credential.create_timestamp.isoformat()
                        if credential.create_timestamp
                        else None,
                        "effective_date": credential.effective_date.isoformat()
                        if credential.effective_date
                        else None,
                        "inactive": credential.inactive,
                        "latest": credential.latest,
                        "revoked": credential.revoked,
                        "revoked_date": credential.revoked_date.isoformat()
                        if credential.revoked_date
                        else None,
                        "credential_id": credential.credential_id,
                        "names": [
                            {
                                "id": name.id,
                                "text": name.text or None,
                                "language": name.language or None,
                                "credential_id": name.credential_id,
                                "type": name.type,
                            } if name else {}
                            for name in credential.topic.get_active_names()
                        ],
                        "local_name": {
                            "id": credential.topic.get_local_name().id,
                            "text": credential.topic.get_local_name().text or None,
                            "language": credential.topic.get_local_name().language
                            or None,
                            "credential_id": credential.topic.get_local_name().credential_id
                            or None,
                            "type": credential.topic.get_local_name().type or None,
                        } if credential.topic.get_local_name() else {},
                        "remote_name": {
                            "id": credential.topic.get_remote_name().id,
                            "text": credential.topic.get_remote_name().text or None,
                            "language": credential.topic.get_remote_name().language
                            or None,
                            "credential_id": credential.topic.get_remote_name().credential_id
                            or None,
                            "type": credential.topic.get_remote_name().type or None,
                        } if credential.topic.get_remote_name() else {},
                        # "addresses": [
                        #     {
                        #         "country": address.country or None,
                        #         "addressee": address.addressee or None,
                        #         "province": address.province or None,
                        #         "create_timestamp": address.create_timestamp.isoformat()
                        #         if address.create_timestamp is not None
                        #         else None,
                        #         "credential_id": address.credential_id or None,
                        #         "civic_address": address.civic_address or None,
                        #         "update_timestamp": address.update_timestamp.isoformat()
                        #         if address.update_timestamp is not None
                        #         else None,
                        #         "id": address.id,
                        #         "postal_code": address.postal_code or None,
                        #         "city": address.city or None,
                        #     }
                        #     for address in credential.addresses.all()
                        # ],
                        "topic": {
                            "id": credential.topic.id,
                            "source_id": credential.topic.source_id,
                            "type": credential.topic.type,
                        },
                        "related_topics": [
                            {
                                "id": related_topic.id,
                                # "create_timestamp": related_topic.create_timestamp
                                # if related_topic.create_timestamp is not None
                                # else None,
                                # "update_timestamp": related_topic.update_timestamp
                                # if related_topic.update_timestamp is not None
                                # else None,
                                "source_id": related_topic.source_id,
                                "type": related_topic.type,
                                "names": [
                                    {
                                        "id": name.id,
                                        "text": name.text or None,
                                        "language": name.language or None,
                                        "credential_id": name.credential_id,
                                        "type": name.type,
                                    } if name else {}
                                    for name in related_topic.get_active_names()
                                ],
                                "local_name": {
                                    "id": related_topic.get_local_name().id,
                                    "text": related_topic.get_local_name().text or None,
                                    "language": related_topic.get_local_name().language
                                    or None,
                                    "credential_id": related_topic.get_local_name().credential_id
                                    or None,
                                    "type": related_topic.get_local_name().type or None,
                                } if related_topic.get_local_name() else {},
                                "remote_name": {
                                    "id": related_topic.get_remote_name().id,
                                    "text": related_topic.get_remote_name().text or None,
                                    "language": related_topic.get_remote_name().language
                                    or None,
                                    "credential_id": related_topic.get_remote_name().credential_id
                                    or None,
                                    "type": related_topic.get_remote_name().type or None,
                                } if related_topic.get_remote_name() else {},
                            } if related_topic else {}
                            for related_topic in credential.related_topics.all()
                        ],
                        "credential_type": {
                            "id": credential.credential_type.id,
                            "description": credential.credential_type.description,
                        },
                    }
                    for credential in credential_set.credentials.all()
                ],
            }
            for credential_set in credential_sets
        ]

        return Response(data)

    def get_object(self):
        if self.kwargs.get("pk"):
            return super(TopicViewSet, self).get_object()

        type = self.kwargs.get("type")
        source_id = self.kwargs.get("source_id")
        if not type or not source_id:
            raise Http404()

        # map type to a schema name, if an "old style" type is used
        if settings.CRED_TYPE_SYNONYMS and type.lower() in settings.CRED_TYPE_SYNONYMS:
            type = settings.CRED_TYPE_SYNONYMS[type.lower()]

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

        # TODO: if the agent was not started with the --auto-verify-presentation flag, verification will need to be initiated
        retries = PROOF_RETRY_MAX_ATTEMPTS
        result = None
        delay = float(PROOF_RETRY_INITIAL_DELAY/1000)
        while retries > 0:
            sleep(delay)
            retries -= 1
            delay = delay * PROOF_RETRY_DELAY_BACKOFF
            presentation_state_response = call_agent_with_retry(
                f"{settings.AGENT_ADMIN_URL}/present-proof/records/{presentation_exchange_id}",
                post_method=False,
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
    apply_custom_methods(
        TopicRelationshipViewSet, "views", "TopicRelationshipViewSet", "includeMethods"
    )
except:
    pass
