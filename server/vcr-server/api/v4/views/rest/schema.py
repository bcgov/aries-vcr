from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters import rest_framework as filters

from api.v2.models.CredentialType import Schema

from api.v4.serializers.rest.credential import SchemaSerializer


class RestView(ReadOnlyModelViewSet):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()
    filter_backends = (filters.DjangoFilterBackend,) 
    filterset_fields = ("name", "origin_did")

    def list(self, request):
        paging = request.query_params.get("paging", None)
        if paging and paging == "false":
            self.pagination_class = None
        response = super(ReadOnlyModelViewSet, self).list(request)
        item_count = self.queryset.count()
        response["item_count"] = item_count
        return response
