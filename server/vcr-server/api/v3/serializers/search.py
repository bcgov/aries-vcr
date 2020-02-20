import logging

from rest_framework.serializers import CharField, SerializerMethodField
from drf_haystack.serializers import (
    HaystackFacetSerializer,
    HaystackSerializerMixin,
    HaystackSerializer,
)

from ..indexes.Address import AddressIndex
from ..indexes.Name import NameIndex

from api.v2.models.Address import Address
from api.v2.models.Name import Name

from api.v2.serializers.rest import NameSerializer, AddressSerializer


logger = logging.getLogger(__name__)


class NameAutocompleteSerializer(HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "name"

    @staticmethod
    def get_value(obj):
        return obj.name_text

    class Meta(NameSerializer.Meta):
        index_classes = [NameIndex]
        fields = ("type", "value")


class AddressAutocompleteSerializer(HaystackSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "address"

    @staticmethod
    def get_value(obj):
        return obj.address_civic_address

    class Meta(AddressSerializer.Meta):
        index_classes = [AddressIndex]
        fields = ("type", "value")


class AggregateAutocompleteSerializer(HaystackSerializer):
    class Meta:
        serializers = {
            AddressIndex: AddressAutocompleteSerializer,
            NameIndex: NameAutocompleteSerializer,
        }

        filter_fields_map = {
            "inactive": ("address_credential_inactive", "name_credential_inactive"),
            "revoked": ("address_credential_revoked", "name_credential_revoked"),
        }
