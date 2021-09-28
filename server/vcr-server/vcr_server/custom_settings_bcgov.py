"""
Enclose property names in double quotes in order to JSON serialize the contents in the API
"""
import logging

from rest_framework.decorators import action

LOGGER = logging.getLogger(__name__)


@action(detail=True, url_path="related_to_relations")
def list_related_to_relations(self, request, pk=None):
    # We load most at runtime because ORM isn't loaded at setup time
    from api.v2.serializers.search import CustomTopicRelationshipSerializer
    from api.v2.models.TopicRelationship import TopicRelationship
    from rest_framework.response import Response

    topic_relationships = TopicRelationship.objects.filter(topic=pk).all()

    data = [
        {
            "topic_id": topic_relationship.topic_id,
            "relation_id": topic_relationship.id,
            "credential": {
                "id": topic_relationship.credential.id,
                "create_timestamp": topic_relationship.credential.create_timestamp.isoformat()
                if topic_relationship.credential.create_timestamp
                else None,
                "effective_date": topic_relationship.credential.effective_date.isoformat()
                if topic_relationship.credential.effective_date
                else None,
                "inactive": topic_relationship.credential.inactive,
                "latest": topic_relationship.credential.latest,
                "revoked": topic_relationship.credential.revoked,
                "revoked_date": topic_relationship.credential.revoked_date.isoformat()
                if topic_relationship.credential.revoked_date
                else None,
                "credential_id": topic_relationship.credential.credential_id,
                "credential_type": {
                    "id": topic_relationship.credential.credential_type.id,
                    "description": topic_relationship.credential.credential_type.description,
                    "schema_label": topic_relationship.credential.credential_type.schema_label,
                    "schema_description": topic_relationship.credential.credential_type.schema_description,
                    "credential_title": topic_relationship.credential.credential_type.credential_title,
                    "highlighted_attributes": topic_relationship.credential.credential_type.highlighted_attributes,

                },
            },
            "attributes": [
                {
                    "id": attribute.id,
                    "type": attribute.type or None,
                    "format": attribute.format or None,
                    "value": attribute.value or None,
                }
                for attribute in topic_relationship.credential_attributes
            ],
            "topic": {
                "id": topic_relationship.topic.id,
                "create_timestamp": topic_relationship.topic.create_timestamp,
                "source_id": topic_relationship.topic.source_id,
                "type": topic_relationship.topic.type,
                "names": [
                    {
                        "id": name.id,
                        "text": name.text or None,
                        "language": name.language or None,
                        "credential_id": name.credential_id,
                        "type": name.type,
                    }
                    for name in topic_relationship.topic.get_active_names()
                ],
            },
            "related_topic": {
                "id": topic_relationship.related_topic.id,
                "create_timestamp": topic_relationship.related_topic.create_timestamp,
                "source_id": topic_relationship.related_topic.source_id,
                "type": topic_relationship.related_topic.type,
                "names": [
                    {
                        "id": name.id,
                        "text": name.text or None,
                        "language": name.language or None,
                        "credential_id": name.credential_id,
                        "type": name.type,
                    }
                    for name in topic_relationship.related_topic.get_active_names()
                ],
            },
        }
        for topic_relationship in topic_relationships
    ]
    item_count = len(data)
    response = Response(data)
    response["item_count"] = item_count
    return response


@action(detail=True, url_path="related_from_relations")
def list_related_from_relations(self, request, pk=None):
    # We load most at runtime because ORM isn't loaded at setup time
    from api.v2.serializers.search import CustomTopicRelationshipSerializer
    from api.v2.models.TopicRelationship import TopicRelationship
    from rest_framework.response import Response

    parent_queryset = TopicRelationship.objects.filter(related_topic=pk).all()
    serializer = CustomTopicRelationshipSerializer(
        parent_queryset, many=True, relationship_type="from"
    )
    item_count = parent_queryset.count()
    response = Response(serializer.data)
    response["item_count"] = item_count
    return response


TIME_ZONE = "America/Vancouver"

CUSTOMIZATIONS = {
    "serializers": {
        "Address": {
            "includeFields": [
                "id",
                "create_timestamp",
                "update_timestamp",
                "addressee",
                "civic_address",
                "city",
                "province",
                "postal_code",
                "country",
                "credential",
            ]
        },
        "Topic": {
            "includeFields": [
                "id",
                "create_timestamp",
                "update_timestamp",
                "source_id",
                "type",
                "related_to",
                "related_from",
            ]
        },
        "TopicRelationship": {
            "includeFields": ["id", "credential", "topic", "related_topic"]
        },
    },
    "views": {
        "TopicRelationshipViewSet": {
            "includeMethods": [list_related_to_relations, list_related_from_relations]
        },
    },
}
