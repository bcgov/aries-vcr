import logging
from collections import OrderedDict

from rest_framework.serializers import CharField, DateTimeField, IntegerField, SerializerMethodField
from drf_haystack.serializers import HaystackSerializer, HaystackFacetSerializer

from api.v2.models.Address import Address
from api.v2.models.Credential import Credential
from api.v2.models.CredentialType import CredentialType
from api.v2.models.Issuer import Issuer
from api.v2.models.Name import Name
from api.v2.models.Topic import Topic

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
    id = IntegerField(source="object.id")
    source_id = CharField(source="object.source_id")
    type = CharField(source="object.type")
    names = TopicNameSerializer(
        source="object.get_active_names", many=True)
    addresses = TopicAddressSerializer(
        source="object.get_active_addresses", many=True)
    attributes = TopicAttributeSerializer(
        source="object.get_active_attributes", many=True)
    credential_set = CredentialSetSerializer(
        source="object.foundational_credential.credential_set")
    credential_type = CredentialTypeSerializer(
        source="object.foundational_credential.credential_type")
    effective_date = DateTimeField(
        source="object.foundational_credential.effective_date")
    revoked_date = DateTimeField(
        source="object.foundational_credential.revoked_date")

    class Meta:
        index_classes = [TopicIndex]
        fields = ("id", "source_id", "type", "names", "addresses", "attributes",
                  "credential_set", "credential_type", "effective_date", "revoked_date")
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
        field_memo = self.format_facet_text(field_name, facets)
        return [self.format_facet_field(field_name, facet, field_memo) for facet in facets]

    def format_facet_text(self, field_name, facets):
        values = [facet[0] for facet in facets]
        Model, field_selector, text = None, "", {}
        if field_name == "issuer_id":
            Model, field_selector = Issuer, "name"
        elif field_name == "type_id":
            Model, field_selector = CredentialType, "description"

        if Model and field_selector:
            rows = Model.objects.filter(pk__in=values)
            if len(rows):
                text = {
                    field_name: {
                        str(row['id']): row[field_selector] for row in rows.values()
                    }
                }

        return text

    def format_facet_field(self, field_name, facet, field_memo):
        text, value, count = None, facet[0], facet[1]
        if field_name in field_memo and value in field_memo[field_name]:
            text = field_memo[field_name][value]
        return {"value": value, "count": count, "text": text}

    class Meta:
        index_classes = [TopicIndex]
        fields = ("topic_category", "topic_type_id", "topic_issuer_id")
        field_options = {
            "topic_category": {},
            "topic_type_id": {},
            "topic_issuer_id": {},
        }
