import logging
from collections import OrderedDict

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
from api.v2.serializers.search import (
    CredentialFacetSerializer,
)

from api.v3.indexes.Topic import TopicIndex


facet_filter_display_map = {
    'topic_category': 'category',
    'topic_type_id': 'type_id',
    'topic_issuer_id': 'issuer_id'
}


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
        # ExactFilter fields
        exact_fields = ("topic_issuer_id", "topic_type_id")
        # StatusFilter fields
        status_fields = {"topic_inactive": "false", "topic_revoked": "false"}
        # HaystackFilter fields
        search_fields = ("score")


class FacetSerializer(CredentialFacetSerializer):

    def get_facets(self, instance):
        result = OrderedDict()
        for facet_type, facet_data in instance.items():
            serial_data = {}
            for field, facets in facet_data.items():
                if field in facet_filter_display_map:
                    field = facet_filter_display_map[field]
                serial_data[field] = self.format_facets(field, facets)
            result[facet_type] = serial_data
        return result

    def format_facets(self, field_name, facets):
        return [{"value": facet[0], "count": facet[1]} for facet in facets]

    class Meta:
        index_classes = [TopicIndex]
        fields = ("topic_category", "topic_type_id", "topic_issuer_id")
        field_options = {
            "topic_category": {},
            "topic_type_id": {},
            "topic_issuer_id": {},
        }
