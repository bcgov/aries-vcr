
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

    @swagger_auto_schema(responses={200: CredentialSetSerializer(many=True)})
    @action(detail=True, url_path="credential-set", methods=["get"])
    def list_credential_sets(self, request, pk=None):
        item = self.get_object()

        credential_sets = (
            item.credential_sets
            .prefetch_related(
                "credentials__attributes",
                "credentials__names",
                "credentials__credential_type",
                "credentials__credential_type__issuer"
            )
            .order_by("first_effective_date")
            .all()
        )

        data = [
            {
                "id": credential_set.id,
                "create_timestamp": credential_set.create_timestamp.isoformat()
                if credential_set.create_timestamp is not None else None,
                "update_timestamp": credential_set.update_timestamp.isoformat()
                if credential_set.update_timestamp is not None else None,
                "latest_credential_id": credential_set.latest_credential_id,
                "first_effective_date": credential_set.first_effective_date.isoformat()
                if credential_set.first_effective_date is not None else None,
                "last_effective_date": credential_set.last_effective_date.isoformat()
                if credential_set.last_effective_date is not None else None,
                "credentials": [
                    CredentialSerializer(credential).data
                    for credential in credential_set.credentials.all()
                ],
            }
            for credential_set in credential_sets
        ]

        return Response(data)

    def get_object(self):
        if self.kwargs.get("pk"):
            return super(RestView, self).get_object()

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
