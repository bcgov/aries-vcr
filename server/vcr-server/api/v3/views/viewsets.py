from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class RetriveOnlyModelViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """
    A viewset that provides default `retrieve()` action.
    """

    pass
