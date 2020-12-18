import logging

from rest_framework.serializers import SerializerMethodField
from drf_haystack.serializers import HaystackFacetSerializer

from api.v2.models import Credential

from api.v2.serializers.rest import (
    ExpandedCredentialSerializer,
    TopicSerializer
)

from api.v3.indexes.Topic import TopicIndex

from api.v3.serializers.search import TopicSearchSerializerBase

logger = logging.getLogger(__name__)


class SearchSerializer(TopicSearchSerializerBase):
    # TODO: Format response outputs porperly

    class Meta(TopicSerializer.Meta):
        index_classes = [TopicIndex]
        fields = ("type", "sub_type", "value", "score", "topic_source_id", "topic_type",
                  "topic_name", "topic_address", "credential_id", "credential_type")


class FacetSerializer(HaystackFacetSerializer):
    # TODO: Format facet outputs porperly
    serialize_objects = True

    class Meta:
        index_classes = [TopicIndex]
        fields = ("topic_category", "topic_type_id", "topic_issuer_id")
        field_options = {
            "topic_category": {},
            "topic_type_id": {},
            "topic_issuer_id": {},
        }
