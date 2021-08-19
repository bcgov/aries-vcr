from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v2.models.CredentialType import CredentialType

from api.v2.serializers.rest import CredentialTypeSerializer

class RestView(ReadOnlyModelViewSet):
    serializer_class = CredentialTypeSerializer
    queryset = CredentialType.objects.all()

    def list(self, request):
        paging = request.query_params.get("paging", None)
        if (paging and paging == 'false'):
            self.pagination_class = None
        return super(ReadOnlyModelViewSet, self).list(request)