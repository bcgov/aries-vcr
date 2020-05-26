import logging

from rest_framework.serializers import CharField, SerializerMethodField
from drf_haystack.serializers import (
    HaystackFacetSerializer,
    HaystackSerializerMixin,
    HaystackSerializer,
)

from ..indexes.Address import AddressIndex
from ..indexes.Name import NameIndex
from ..indexes.Topic import TopicIndex

from api.v2.models.Address import Address
from api.v2.models.Name import Name

from api.v2.serializers.rest import NameSerializer, AddressSerializer


logger = logging.getLogger(__name__)


class NameAutocompleteSerializer(HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()
    score = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "name"

    @staticmethod
    def get_value(obj):
        return obj.name_text

    @staticmethod
    def get_score(obj):
        return obj.score

    class Meta(NameSerializer.Meta):
        index_classes = [NameIndex]
        fields = ("type", "value", "score")


class AddressAutocompleteSerializer(HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()
    score = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "address"

    @staticmethod
    def get_value(obj):
        return obj.address_civic_address

    @staticmethod
    def get_score(obj):
        return obj.score

    class Meta(AddressSerializer.Meta):
        index_classes = [AddressIndex]
        fields = ("type", "value", "score")


class TopicAutocompleteSerializer(HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()
    score = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "topic"

    @staticmethod
    def get_value(obj):
        return obj.topic_source_id

    @staticmethod
    def get_score(obj):
        return obj.score

    class Meta(AddressSerializer.Meta):
        index_classes = [TopicIndex]
        fields = ("type", "value", "score")


class AggregateAutocompleteSerializer(HaystackSerializer):
    class Meta:
        serializers = {
            AddressIndex: AddressAutocompleteSerializer,
            NameIndex: NameAutocompleteSerializer,
            TopicIndex: TopicAutocompleteSerializer,
        }

        filter_fields_map = {
            "inactive": (
                "address_credential_inactive",
                "name_credential_inactive",
                "topic_all_credentials_inactive",
            ),
            "revoked": (
                "address_credential_revoked",
                "name_credential_revoked",
                "topic_all_credentials_revoked",
            ),
        }
