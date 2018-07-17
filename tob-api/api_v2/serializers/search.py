from drf_haystack.serializers import (
    HaystackSerializerMixin,
    HaystackSerializer,
)

from rest_framework.serializers import ListSerializer, SerializerMethodField

from django.db.models.manager import Manager

from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnDict

from api_v2.serializers.rest import (
    AddressSerializer,
    NameSerializer,
    ContactSerializer,
    PersonSerializer,
    TopicSerializer,
    CredentialSerializer,
    IssuerSerializer,
)

from api_v2.search_indexes import TopicIndex

from api_v2.models.Name import Name
from api_v2.models.Address import Address
from api_v2.models.Person import Person
from api_v2.models.Contact import Contact


class SearchResultsListSerializer(ListSerializer):
    @staticmethod
    def __camelCase(s):
        return s[:1].lower() + s[1:] if s else ""

    def __get_keyName(self, instance):
        searchIndex = instance.searchindex
        model = searchIndex.get_model()
        return self.__camelCase(model.__name__) + "s"

    @property
    def data(self):
        ret = super(ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        results = OrderedDict()
        iterable = data.all() if isinstance(data, Manager) else data
        for item in iterable:
            searchIndexName = self.__get_keyName(item)
            results.setdefault(searchIndexName, []).append(
                self.child.to_representation(item)
            )

        return results


class CustomCredentialSerializer(CredentialSerializer):
    # topics = CustomTopicSerializer(read_only=True, many=True)

    class Meta(CredentialSerializer.Meta):
        # depth =
        fields = ("id", "start_date", "end_date")


class CustomIssuerSerializer(IssuerSerializer):
    class Meta(IssuerSerializer.Meta):
        fields = ("id", "did", "name", "abbreviation", "email", "url")


class CustomAddressSerializer(AddressSerializer):
    last_updated = SerializerMethodField()
    # issuer = SerializerMethodField()

    class Meta(AddressSerializer.Meta):
        fields = (
            "id",
            "credential",
            "last_updated",
            "addressee",
            "civic_address",
            "city",
            "province",
            "postal_code",
            "country",
            # "type"
            # "issuer"
        )

    def get_last_updated(self, obj):
        return obj.credential.start_date

    def get_issuer(self, obj):
        serializer = CustomIssuerSerializer(
            instance=obj.credential.credential_type.issuer
        )
        return serializer.data


class CustomNameSerializer(NameSerializer):
    last_updated = SerializerMethodField()
    issuer = SerializerMethodField()

    class Meta(NameSerializer.Meta):
        fields = (
            "id",
            "credential",
            "last_updated",
            "text",
            "language",
            "issuer",
        )

    def get_last_updated(self, obj):
        return obj.credential.start_date

    def get_issuer(self, obj):
        serializer = CustomIssuerSerializer(
            instance=obj.credential.credential_type.issuer
        )
        return serializer.data


class CustomContactSerializer(ContactSerializer):
    last_updated = SerializerMethodField()
    # issuer = SerializerMethodField()

    class Meta(ContactSerializer.Meta):
        fields = ("id", "credential", "last_updated", "text", "type")

    def get_last_updated(self, obj):
        return obj.credential.start_date

    def get_issuer(self, obj):
        serializer = CustomIssuerSerializer(
            instance=obj.credential.credential_type.issuer
        )
        return serializer.data


class CustomPersonSerializer(PersonSerializer):
    last_updated = SerializerMethodField()
    # issuer = SerializerMethodField()

    class Meta(PersonSerializer.Meta):
        fields = ("id", "credential", "last_updated", "full_name")

    def get_last_updated(self, obj):
        return obj.credential.start_date

    def get_issuer(self, obj):
        serializer = CustomIssuerSerializer(
            instance=obj.credential.credential_type.issuer
        )
        return serializer.data


class CustomTopicSerializer(TopicSerializer):
    names = SerializerMethodField()
    addresses = SerializerMethodField()
    contacts = SerializerMethodField()
    people = SerializerMethodField()

    class Meta(TopicSerializer.Meta):
        depth = 1
        fields = (
            "id",
            "source_id",
            "type",
            "names",
            "addresses",
            "contacts",
            "people",
        )

    def get_names(self, obj):
        credential_ids = (
            obj.direct_credentials()
            .filter(end_date=None)
            .values_list("id", flat=True)
        )
        names = Name.objects.filter(credential__id__in=credential_ids)
        serializer = CustomNameSerializer(instance=names, many=True)
        return serializer.data

    def get_addresses(self, obj):
        credential_ids = (
            obj.direct_credentials()
            .filter(end_date=None)
            .values_list("id", flat=True)
        )
        addresses = Address.objects.filter(credential__id__in=credential_ids)
        serializer = CustomAddressSerializer(instance=addresses, many=True)
        return serializer.data

    def get_contacts(self, obj):
        credential_ids = (
            obj.direct_credentials()
            .filter(end_date=None)
            .values_list("id", flat=True)
        )
        contacts = Contact.objects.filter(credential__id__in=credential_ids)
        serializer = CustomContactSerializer(instance=contacts, many=True)
        return serializer.data

    def get_people(self, obj):
        credential_ids = (
            obj.direct_credentials()
            .filter(end_date=None)
            .values_list("id", flat=True)
        )
        people = Person.objects.filter(credential__id__in=credential_ids)
        serializer = CustomPersonSerializer(instance=people, many=True)
        return serializer.data


class TopicSearchSerializer(HaystackSerializerMixin, CustomTopicSerializer):
    class Meta(CustomTopicSerializer.Meta):
        pass


class TopicSearchResultsSerializer(HaystackSerializer):
    class Meta:
        # index_classes = [TopicIndex]
        # list_serializer_class = SearchResultsListSerializer
        search_fields = ("name", "location")
        serializers = {TopicIndex: TopicSearchSerializer}
