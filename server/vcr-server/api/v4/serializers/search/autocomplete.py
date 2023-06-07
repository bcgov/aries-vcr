# DEPRECATED: this should not be used in new code and will be removed imminently

from rest_framework.serializers import SerializerMethodField

from api.v3.indexes.Topic import TopicIndex

from api.v2.serializers.rest import TopicSerializer

from api.v3.serializers.search import (
    TopicAutocompleteSerializer as V3TopicAutocompleteSerializer,
)


class TopicAutocompleteSerializer(V3TopicAutocompleteSerializer):
    names = SerializerMethodField()

    @staticmethod
    def get_names(obj):
        return [
            name.text
            for name in obj.object.get_active_names()
            if name.type == "entity_name"
        ]

    class Meta(TopicSerializer.Meta):
        index_classes = [TopicIndex]
        fields = ("id", "type", "sub_type", "value", "score", "topic_source_id",
                  "topic_type", "credential_id", "credential_type", "names",)
