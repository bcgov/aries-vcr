from rest_framework import permissions

from drf_haystack.viewsets import HaystackViewSet

from api.v2.models.Topic import Topic

from api.v4.serializers.search.topic import SearchSerializer as TopicSearchSerializer


class SearchView(HaystackViewSet):
    """
    Provide Topic search via Solr with both faceted (/facets) and unfaceted results
    """

    permission_classes = (permissions.AllowAny,)

    index_models = [Topic]

    serializer_class = TopicSearchSerializer
