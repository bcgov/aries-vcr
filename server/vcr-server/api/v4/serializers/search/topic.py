import logging

from rest_framework.serializers import SerializerMethodField
from drf_haystack.serializers import HaystackSerializer, HaystackFacetSerializer

from api.v2.models import Address, Credential, Name, Topic

from api.v2.serializers.rest import (
    AddressSerializer,
    CredentialSerializer,
    CredentialSetSerializer,
    CredentialTypeSerializer,
    NameSerializer,
    TopicSerializer,
    TopicAttributeSerializer,
)

from api.v3.indexes.Topic import TopicIndex


class TopicNameSerializer(NameSerializer):

    credential_id = SerializerMethodField()

    @staticmethod
    def get_credential_id(obj):
        return obj.credential.id

    class Meta(NameSerializer.Meta):
        fields = ("id", "text", "language", "type", "credential_id")


class TopicAddressSerializer(AddressSerializer):

    credential_id = SerializerMethodField()

    @staticmethod
    def get_credential_id(obj):
        return obj.credential.id

    class Meta(AddressSerializer.Meta):
        fields = ("id", "addressee", "civic_address", "city",
                  "province", "postal_code", "country", "credential_id")


class SearchSerializer(HaystackSerializer):
    source_id = SerializerMethodField()
    names = TopicNameSerializer(source="object.get_active_names", many=True)
    addresses = TopicAddressSerializer(source="object.get_active_addresses", many=True)
    attributes = TopicAttributeSerializer(
        source="object.get_active_attributes", many=True)
    credential_set = CredentialSetSerializer(
        source="object.foundational_credential.credential_set")
    credential_type = CredentialTypeSerializer(
        source="object.foundational_credential.credential_type")

    @staticmethod
    def get_source_id(obj):
        return obj.topic_source_id

    class Meta:
        index_classes = [TopicIndex]
        fields = ("source_id", "names", "addresses", "attributes",
                  "credential_set", "credential_type")


class FacetSerializer(HaystackFacetSerializer):
    # TODO: Format facet outputs porperly
    serialize_objects = True

    class Meta:
        index_classes = [TopicIndex]
        fields = ("topic_category", "topic_type_id", "topic_issuer_id")
        field_options = {
            "topic_category": {},
            "topic_type_id": {},
            "topic_issuer_id": {},
        }
