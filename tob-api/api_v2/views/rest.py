from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api_v2.serializers import (
    IssuerSerializer,
    SchemaSerializer,
    CredentialTypeSerializer,
)
from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.models.CredentialType import CredentialType


class IssuerViewSet(ViewSet):
    def list(self, request):
        queryset = Issuer.objects.all()
        serializer = IssuerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Issuer.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = IssuerSerializer(item)
        return Response(serializer.data)


class SchemaViewSet(ViewSet):
    def list(self, request):
        queryset = Schema.objects.all()
        serializer = SchemaSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Schema.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SchemaSerializer(item)
        return Response(serializer.data)


class CredentialTypeViewSet(ViewSet):
    def list(self, request):
        queryset = CredentialType.objects.all()
        serializer = CredentialTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = CredentialType.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CredentialTypeSerializer(item)
        return Response(serializer.data)
