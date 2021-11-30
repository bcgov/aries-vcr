from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters import rest_framework as filters
import json

from drf_yasg.utils import swagger_auto_schema


from api.v2.models.CredentialType import Issuer, Schema

from api.v4.serializers.rest.credential import SchemaSerializer


class RestView(ReadOnlyModelViewSet):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name", "origin_did")

    @swagger_auto_schema(responses={200: SchemaSerializer(many=True)})
    def list(self, request):
        data = SchemaSerializer(self.queryset, many=True).data
        cred_type_x_schema = {}
        for schema in data:
            key = f"{schema['name']}:{schema['origin_did']}"
            if not key in cred_type_x_schema:
                cred_type_x_schema[key] = []
            [cred_type_x_schema[key].append(x) for x in schema['credential_types']]
        return Response(cred_type_x_schema)