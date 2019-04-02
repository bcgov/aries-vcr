from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_hooks.models import Hook

from api_v2.models.Subscription import Subscription
from api_v2.serializers.hooks import (
    HookSerializer,
    RegistrationSerializer,
    SubscriptionSerializer,
)

SUBSCRIBERS_GROUP_NAME = "subscriber"


class RegistrationViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    # queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    lookup_field = "username"
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)
    permission_classes = ()

    def get_queryset(self):
        return (
            get_user_model().objects.filter(groups__name=SUBSCRIBERS_GROUP_NAME).all()
        )

    def perform_create(self, serializer):
        serializer.save()

class SubscriptionViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    # queryset = Subscription.objects.filter(owner__username=self.kwargs['username']).all()
    serializer_class = SubscriptionSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)
    permission_classes = ()

    def get_queryset(self):
        return Subscription.objects.filter(
            owner__username=self.kwargs["registration_username"]
        ).all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HookViewSet(ModelViewSet):
    """
    Retrieve, create, update or destroy webhooks.
    """

    queryset = Hook.objects.all()
    model = Hook
    serializer_class = HookSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
