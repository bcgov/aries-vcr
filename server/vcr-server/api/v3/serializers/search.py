import logging

from rest_framework.serializers import SerializerMethodField
from drf_haystack.serializers import HaystackFacetSerializer, HaystackSerializerMixin, HaystackSerializer

from ..indexes.Address import AddressIndex
from ..indexes.Name import NameIndex
from ..indexes.Topic import TopicIndex

from api.v2.models.Address import Address
from api.v2.models.Name import Name

from api.v2.serializers.rest import (
    NameSerializer,
    AddressSerializer,
)
from api.v3.serializers.rest import (
    TopicSerializer
)


logger = logging.getLogger(__name__)


class AutocompleteSerializerBase():

    @staticmethod
    def get_score(obj):
        return obj.score

    @staticmethod
    def get_topic_source_id(obj):
        return obj._object.credential.topic.source_id

    # DEPRECATED
    @staticmethod
    def get_topic_type(obj):
        return obj._object.credential.topic.type

    @staticmethod
    def get_credential_id(obj):
        return obj._object.credential.credential_id

    @staticmethod
    def get_credential_type(obj):
        return obj._object.credential.credential_type.description


class NameAutocompleteSerializer(AutocompleteSerializerBase, HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()
    score = SerializerMethodField()
    topic_source_id = SerializerMethodField()
    # DEPRECATED
    topic_type = SerializerMethodField()
    credential_type = SerializerMethodField()
    credential_id = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "name"

    @staticmethod
    def get_value(obj):
        return obj.name_text

    class Meta(NameSerializer.Meta):
        index_classes = [NameIndex]
        fields = ("type", "value", "score", "topic_source_id",
                  "topic_type", "credential_id", "credential_type")


class AddressAutocompleteSerializer(AutocompleteSerializerBase, HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()
    score = SerializerMethodField()
    topic_source_id = SerializerMethodField()
    # DEPRECATED
    topic_type = SerializerMethodField()
    credential_id = SerializerMethodField()
    credential_type = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "address"

    @staticmethod
    def get_value(obj):
        return obj.address_civic_address

    class Meta(AddressSerializer.Meta):
        index_classes = [AddressIndex]
        fields = ("type", "value", "score", "topic_source_id",
                  "topic_type" "credential_id", "credential_type")


class TopicAutocompleteSerializer(AutocompleteSerializerBase, HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()
    score = SerializerMethodField()
    topic_source_id = SerializerMethodField()
    # DEPRECATED
    topic_type = SerializerMethodField()
    credential_id = SerializerMethodField()
    credential_type = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "topic"

    @staticmethod
    def get_value(obj):
        return obj.topic_source_id

    @staticmethod
    def get_topic_source_id(obj):
        return obj._object.source_id

    # DEPRECATED
    @staticmethod
    def get_topic_type(obj):
        return obj._object.type

    @staticmethod
    def get_credential_id(obj):
        return obj._object.foundational_credential.credential_id

    @staticmethod
    def get_credential_type(obj):
        return obj._object.foundational_credential.credential_type.description

    class Meta(TopicSerializer.Meta):
        index_classes = [TopicIndex]
        fields = ("type", "value", "score", "topic_source_id",
                  "topic_type", "credential_id", "credential_type")


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
