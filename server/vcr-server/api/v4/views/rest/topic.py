from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v2.models.Topic import Topic

from api.v2.serializers.rest import CredentialSetSerializer, TopicSerializer

from api.v4.serializers.rest.credential import RestSerializer as CredentialSerializer


class RestView(ReadOnlyModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def list(self, request):
        response = super().list(request)
        item_count = self.queryset.count()
        response["item_count"] = item_count
        return response

    @swagger_auto_schema(responses={200: CredentialSetSerializer(many=True)})
    @action(detail=True, url_path="credential-set", methods=["get"])
    def credential_set_list(self, request, *args, **kwargs):
        item = self.get_object()

        credential_sets = (
            item.credential_sets.prefetch_related(
                "credentials__attributes",
                "credentials__names",
                "credentials__credential_type",
                "credentials__credential_type__issuer",
            )
            .order_by("first_effective_date")
            .all()
        )

        data = [
            {
                "id": credential_set.id,
                "create_timestamp": (
                    credential_set.create_timestamp.isoformat()
                    if credential_set.create_timestamp is not None
                    else None
                ),
                "update_timestamp": (
                    credential_set.update_timestamp.isoformat()
                    if credential_set.update_timestamp is not None
                    else None
                ),
                "latest_credential_id": credential_set.latest_credential_id,
                "first_effective_date": (
                    credential_set.first_effective_date.isoformat()
                    if credential_set.first_effective_date is not None
                    else None
                ),
                "last_effective_date": (
                    credential_set.last_effective_date.isoformat()
                    if credential_set.last_effective_date is not None
                    else None
                ),
                "credentials": [
                    CredentialSerializer(credential).data
                    for credential in credential_set.credentials.all()
                ],
            }
            for credential_set in credential_sets
        ]

        response = Response(data)
        response["item_count"] = len(data)
        return response

    @swagger_auto_schema(operation_id="topic_type_read")
    @action(
        detail=False,
        url_path="(?P<source_id>[^/.]+)/type/(?P<type>[^/]+)",
        methods=["get"],
    )
    def read(self, request, *args, **kwargs):
        item = self.get_object()
        return Response(self.get_serializer(item).data)

    @action(
        detail=False,
        methods=["get"],
        url_path="(?P<source_id>[^/.]+)/type/(?P<type>[^/]+)/credential/(?P<credential_id>[^/.]+)",
    )
    def raw_credential_read(self, request, *args, **kwargs):
        item = self.get_object()

        credential_id = self.kwargs.get("credential_id")

        credential = item.credentials.filter(
            format="vc_di", credential_id=credential_id, revoked=False
        ).first()

        if not (credential and credential.raw_data):
            raise Http404()

        return Response(credential.raw_data, content_type="application/ld+json")

    def get_object(self):
        if self.kwargs.get("pk"):
            return super(RestView, self).get_object()

        source_id = self.kwargs.get("source_id")
        type = self.kwargs.get("type")
        if not type or not source_id:
            raise Http404()

        # Map type to a schema name, if an "old style" type is used
        if settings.CRED_TYPE_SYNONYMS and type.lower() in settings.CRED_TYPE_SYNONYMS:
            type = settings.CRED_TYPE_SYNONYMS[type.lower()]

        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, source_id=source_id, type=type)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
