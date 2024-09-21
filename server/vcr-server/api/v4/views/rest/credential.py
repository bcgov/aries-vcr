from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.v2.models.Credential import Credential

from api.v4.serializers.rest.credential import CredentialSerializer, RawCredentialSerializer

class RestView(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()
    lookup_field = "credential_id"

    def get_serializer_class(self):
        if self.request.query_params.get("raw_data", None) == "true":
            return RawCredentialSerializer
        return CredentialSerializer

    def get_object(self):
        credential_id = self.kwargs.get("credential_id", None)

        if not credential_id:
            raise Http404()

        filter = {"credential_id": credential_id}
        # If the input parameter is a pure int, treat as an internal database pk
        try:
            filter = {"pk": int(credential_id)}
        except (ValueError, TypeError):
            pass

        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, **filter)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
    
        return obj