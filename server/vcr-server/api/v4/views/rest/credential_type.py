from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v2.models.CredentialType import CredentialType

from api.v4.serializers.rest.credential import CredentialTypeClaimLabelsSerializer


class RestView(ReadOnlyModelViewSet):
    serializer_class = CredentialTypeClaimLabelsSerializer
    queryset = CredentialType.objects.all()

    def list(self, request):
        paging = request.query_params.get("paging", None)
        if paging and paging == "false":
            self.pagination_class = None
        response = super(ReadOnlyModelViewSet, self).list(request)
        item_count = self.queryset.count()
        response["item_count"] = item_count
        return response
