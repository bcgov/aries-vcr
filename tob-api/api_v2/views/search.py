from rest_framework import permissions
from rest_framework.mixins import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView

from api_v2.serializers.search import TopicSearchResultsSerializer
from api_v2.models.Topic import Topic


class TopicSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [Topic]
    serializer_class = TopicSearchResultsSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
