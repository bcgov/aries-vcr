import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import FormParser
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from api_v2.models.User import User
from api_v2.models.Subscription import Subscription
from api_v2.serializers.hooks import *


class RegistrationViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    lookup_field = 'username'
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)
    permission_classes = ()

    def perform_create(self, serializer):
        serializer.save()

class SubscriptionViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    #queryset = Subscription.objects.filter(owner__username=self.kwargs['username']).all()
    serializer_class = SubscriptionSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)
    permission_classes = ()

    def get_queryset(self):
        return Subscription.objects.filter(owner__username=self.kwargs['registration_username']).all()
    
    def perform_create(self, serializer):
        serializer.save()

