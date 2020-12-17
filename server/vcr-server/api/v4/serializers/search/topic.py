import logging

from api.v2.serializers.rest import TopicSerializer

from api.v3.indexes.Topic import TopicIndex

from api.v3.serializers.search import TopicSearchSerializerBase

logger = logging.getLogger(__name__)


class SearchSerializer(TopicSearchSerializerBase):

    class Meta(TopicSerializer.Meta):
        index_classes = [TopicIndex]
        fields = ("type", "sub_type", "value", "score", "topic_source_id", "topic_type",
                  "topic_name", "topic_address", "credential_id", "credential_type")
