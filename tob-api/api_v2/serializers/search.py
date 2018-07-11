from drf_haystack.serializers import (
    HaystackSerializerMixin,
    HaystackSerializer,
)

from django.db.models.manager import Manager
from rest_framework.serializers import ListSerializer
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnDict

from api_v2.serializers.rest import (
    NameSerializer,
    TopicSerializer,
    CredentialSerializer,
)

from api_v2.search_indexes import NameIndex


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


class CustomTopicSerializer(TopicSerializer):
    class Meta(TopicSerializer.Meta):
        depth = 1
        fields = ("id", "source_id", "type")


class CustomCredentialSerializer(CredentialSerializer):
    topics = CustomTopicSerializer(read_only=True, many=True)

    class Meta(CredentialSerializer.Meta):
        depth = 1
        fields = ("id", "start_date", "end_date", "topics")


class CustomNameSerializer(NameSerializer):
    credential = CustomCredentialSerializer(read_only=True)

    class Meta(NameSerializer.Meta):
        depth = 1
        fields = ("id", "text", "language", "credential")


class NameSearchSerializer(HaystackSerializerMixin, CustomNameSerializer):
    class Meta(CustomNameSerializer.Meta):
        pass


class NameSearchResultsSerializer(HaystackSerializer):
    class Meta:
        list_serializer_class = SearchResultsListSerializer
        search_fields = ("name",)
        field_aliases = {}
        exclude = tuple()
        serializers = {NameIndex: NameSearchSerializer}
