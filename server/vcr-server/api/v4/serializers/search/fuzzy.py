from rest_framework import serializers
from rest_framework.serializers import Serializer, SerializerMethodField


class SearchSerializer(Serializer):
    id = SerializerMethodField()
    topic_source_id = serializers.CharField()
    topic_issuer_id = serializers.IntegerField()
    topic_type_id = serializers.IntegerField()
    topic_names = SerializerMethodField()
    topic_inactive = serializers.BooleanField()
    topic_revoked = serializers.BooleanField()

    @staticmethod
    def get_id(obj):
        return int(obj['django_id'])

    @staticmethod
    def get_topic_names(obj):
        return [name for name in obj['topic_name']]
