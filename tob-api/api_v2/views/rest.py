from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import detail_route, list_route
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from api_v2.serializers.rest import (
    IssuerSerializer,
    SchemaSerializer,
    CredentialTypeSerializer,
    TopicSerializer,
    CredentialSerializer,
    AddressSerializer,
    ClaimSerializer,
    ContactSerializer,
    NameSerializer,
    CategorySerializer,
    PersonSerializer,
)

from rest_framework.serializers import SerializerMethodField

from api_v2.serializers.search import CustomTopicSerializer

from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Topic import Topic
from api_v2.models.Credential import Credential
from api_v2.models.Address import Address
from api_v2.models.Claim import Claim
from api_v2.models.Contact import Contact
from api_v2.models.Name import Name
from api_v2.models.Person import Person
from api_v2.models.Category import Category


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

    @detail_route(url_path="credentialtype")
    def list_credential_types(self, request, pk=None):
        queryset = CredentialType.objects.filter(issuer__id=pk)
        get_object_or_404(queryset, pk=pk)
        serializer = CredentialTypeSerializer(queryset, many=True)
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


class ExpandedCredentialSerializer(CredentialSerializer):
    credential_type = SerializerMethodField()
    issuer = SerializerMethodField()

    class Meta(CredentialSerializer.Meta):
        depth = 1
        fields = (
            "id",
            "start_date",
            "effective_date",
            "revoked",
            "credential_type",
            "issuer",
            "addresses",
            "categories",
            "names",
            "contacts",
            "people",
            "topics"
        )

    def get_credential_type(self, obj):
        qs = obj.credential_type
        serializer = CredentialTypeSerializer(instance=qs)
        return serializer.data

    def get_issuer(self, obj):
        qs = obj.credential_type.issuer
        serializer = IssuerSerializer(instance=qs)
        return serializer.data


class TopicViewSet(ViewSet):
    def list(self, request):
        queryset = Topic.objects.all()
        serializer = TopicSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Topic.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = TopicSerializer(item)
        return Response(serializer.data)

    @detail_route(url_path="formatted")
    def retrieve_formatted(self, request, pk=None):
        queryset = Topic.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CustomTopicSerializer(item)
        return Response(serializer.data)

    @detail_route(url_path="credential")
    def list_credentials(self, request, pk=None):
        parent_queryset = Topic.objects.all()
        item = get_object_or_404(parent_queryset, pk=pk)
        queryset = item.credentials
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(url_path="credential/active")
    def list_active_credentials(self, request, pk=None):
        parent_queryset = Topic.objects.all()
        item = get_object_or_404(parent_queryset, pk=pk)
        queryset = item.credentials.filter(revoked=False)
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(url_path="credential/historical")
    def list_historical_credentials(self, request, pk=None):
        parent_queryset = Topic.objects.all()
        item = get_object_or_404(parent_queryset, pk=pk)
        # End date not null
        queryset = item.credentials.filter(~Q(revoked=False))
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(url_path="directcredential")
    def list_direct_credentials(self, request, pk=None):
        parent_queryset = Topic.objects.all()
        item = get_object_or_404(parent_queryset, pk=pk)
        queryset = item.direct_credentials()
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(url_path="directcredential/active")
    def list_active_direct_credentials(self, request, pk=None):
        depth = 2
        parent_queryset = Topic.objects.all()
        item = get_object_or_404(parent_queryset, pk=pk)
        queryset = item.direct_credentials().filter(end_date=None)
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(url_path="directcredential/historical")
    def list_historical_direct_credentials(self, request, pk=None):
        parent_queryset = Topic.objects.all()
        item = get_object_or_404(parent_queryset, pk=pk)
        queryset = item.direct_credentials().filter(~Q(end_date=None))
        serializer = ExpandedCredentialSerializer(queryset, many=True)
        return Response(serializer.data)


class CredentialViewSet(ViewSet):
    def list(self, request):
        queryset = Credential.objects.all()
        serializer = CredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Credential.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CredentialSerializer(item)
        return Response(serializer.data)

    @detail_route(url_path="formatted")
    def retrieve_formatted(self, request, pk=None):
        queryset = Credential.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ExpandedCredentialSerializer(item)
        return Response(serializer.data)

    @list_route(url_path="active")
    def list_active(self, request, pk=None):
        queryset = Credential.objects.filter(end_date=None)
        serializer = CredentialSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(url_path="historical")
    def list_historical(self, request, pk=None):
        queryset = Credential.objects.filter(~Q(end_date=None))
        serializer = CredentialSerializer(queryset, many=True)
        return Response(serializer.data)


class AddressViewSet(ViewSet):
    def list(self, request):
        queryset = Address.objects.all()
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Address.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = AddressSerializer(item)
        return Response(serializer.data)


class ClaimViewSet(ViewSet):
    def list(self, request):
        queryset = Claim.objects.all()
        serializer = ClaimSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Claim.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ClaimSerializer(item)
        return Response(serializer.data)


class ContactViewSet(ViewSet):
    def list(self, request):
        queryset = Contact.objects.all()
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Contact.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ContactSerializer(item)
        return Response(serializer.data)


class NameViewSet(ViewSet):
    def list(self, request):
        queryset = Name.objects.all()
        serializer = NameSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Name.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = NameSerializer(item)
        return Response(serializer.data)


class PersonViewSet(ViewSet):
    def list(self, request):
        queryset = Person.objects.all()
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Person.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = PersonSerializer(item)
        return Response(serializer.data)

class CategoryViewSet(ViewSet):
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(item)
        return Response(serializer.data)
