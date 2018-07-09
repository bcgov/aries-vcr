from drf_haystack.serializers import (
    HaystackSerializerMixin,
    HaystackSerializer
)

from api_v2.serializers.rest import NameSerializer
from api_v2.indices import Name as NameIndex


class NameSearchSerializer(HaystackSerializerMixin, NameSerializer):
    class Meta(NameSerializer.Meta):
        search_fields = ("text",)
        field_aliases = {}
        exclude = tuple()


class TopicSearchSerializer(HaystackSerializer):
    class Meta:
        search_fields = ("text",)
        field_aliases = {}
        exclude = tuple()
        serializers = {NameIndex: NameSearchSerializer}
