import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.exceptions import *
from django.http import JsonResponse
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


class IsOwnerOrCreateOnly(BasePermission):
    """
    Permission check for subscription ownership.
    """
    def has_permission(self, request, view):
        print("IsOwnerOrCreateOnly view permission check ...")
        if request.user.is_authenticated:
            print("request.user", request.user)
        else:
            print("request.user is not authenticated")
        ret = super().has_permission(request, view)
        print(" >>> returns ", ret)
        return ret

    def has_object_permission(self, request, view, obj):
        print("IsOwnerOrCreateOnly.has_object_permission()")
        if isinstance(obj, get_user_model()):
            print("user", request.user)
            if request.user.is_authenticated:
                print("obj", obj)
                return obj == request.user
            elif request.method == 'POST':
                # creating a new user is ok
                return True
        print("IsOwnerOrCreateOnly obj permission check returns False")
        return False

class IsOwnerOnly(BasePermission):
    """
    Permission check for subscription ownership.
    """
    def has_permission(self, request, view):
        print("IsOwnerOnly view permission check ...")
        if request.user.is_authenticated:
            print("request.user", request.user)
        else:
            print("request.user is not authenticated")
        ret = super().has_permission(request, view)
        print(" >>> returns ", ret)
        return ret
        
    def has_object_permission(self, request, view, obj):
        print("IsOwnerOnly.has_object_permission()")
        if isinstance(obj, Subscription):
            print("user", request.user)
            if request.user.is_authenticated:
                print("obj.owner", obj.owner)
                return obj.owner == request.user
        print("IsOwnerOnly obj permission check returns False")
        return False

class RegistrationViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = RegistrationSerializer
    lookup_field = 'username'
    permission_classes = (IsOwnerOrCreateOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return get_user_model().objects.filter(groups__name=SUBSCRIBERS_GROUP_NAME, username=self.request.user.username).all()
        else:
            raise NotAuthenticated()

    def get_object(self):
        if self.request.user.is_authenticated:
            if self.request.user.username == self.kwargs["username"]:
                obj = get_object_or_404(self.get_queryset(), username=self.kwargs["username"])
                self.check_object_permissions(self.request, obj)
                return obj
            else:
                raise PermissionDenied()
        else:
            raise NotAuthenticated()

    def perform_create(self, serializer):
        serializer.save()

class SubscriptionViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOnly,)

    def get_queryset(self):
        if 'registration_username' in self.kwargs:
            return Subscription.objects.filter(
                owner__username=self.kwargs["registration_username"]
            ).all()
        elif 'username' in self.kwargs:
            return Subscription.objects.filter(
                owner__username=self.kwargs["username"]
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
