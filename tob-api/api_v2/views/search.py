from rest_framework.mixins import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView

from api_v2.serializers.search import TopicSearchSerializer


class TopicSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = []
    serializer_class = TopicSearchSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
