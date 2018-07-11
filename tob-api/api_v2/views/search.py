from rest_framework.mixins import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView

from api_v2.serializers.search import NameSearchResultsSerializer
from api_v2.models.Name import Name


class NameSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [Name]
    serializer_class = NameSearchResultsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
