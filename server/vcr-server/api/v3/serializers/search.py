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


# class AutocompleteSerializer(HaystackSerializer):
#     _AddressIndex__type = CharField()
#     _NameIndex__type = CharField()

#     def get__AddressIndex__type(self):
#         return "address"

#     def get__NameIndex__type(self):
#         return "name"

#     class Meta:
#         index_classes = [AddressIndex, NameIndex]
#         fields = ["firstname", "lastname", "address", "name"]


class NameAutocompleteSerializer(HaystackSerializer):

    # type = SerializerMethodField()
    # value = SerializerMethodField()

    # @staticmethod
    # def get_type(obj):
    #     return "name"

    # @staticmethod
    # def get_value(obj):
    #     return obj.text

    # def to_representation(self, instance):
    #     logger.info(instance.id)
    #     raise Exception("what")

    class Meta(NameSerializer.Meta):
        index_classes = [NameIndex]
        fields = ("name_text", "name_type")


class AddressAutocompleteSerializer(HaystackSerializerMixin, AddressSerializer):

    type = SerializerMethodField()
    value = SerializerMethodField()

    @staticmethod
    def get_type(obj):
        return "address"

    @staticmethod
    def get_value(obj):
        return obj.civic_address

    class Meta(AddressSerializer.Meta):
        index_classes = [AddressIndex]
        fields = ("value", "type")
