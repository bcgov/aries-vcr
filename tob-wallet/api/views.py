from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import WalletItem
from api.serializers import WalletItemSerializer
from django.contrib.auth.models import User
from api.serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import viewsets


# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'wallet_items': reverse('walletitem-list', request=request, format=format)
    })


class WalletItemViewSet(viewsets.ModelViewSet):
    queryset = WalletItem.objects.all()
    serializer_class = WalletItemSerializer
    # the next line is for DRF tokens, comment out for JWT tokens
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # the next line is for JWT tokens, comment out for DRF tokens
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class WalletItemSearchViewSet(generics.ListAPIView):
    queryset = WalletItem.objects.all()
    serializer_class = WalletItemSerializer
    # the next line is for DRF tokens, comment out for JWT tokens
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # the next line is for JWT tokens, comment out for DRF tokens
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg_1 = "wallet_name"
    lookup_url_kwarg_2 = "item_type"

    def get_queryset(self):
        req_wallet = self.kwargs.get(self.lookup_url_kwarg_1)
        req_item_type = self.kwargs.get(self.lookup_url_kwarg_2)
        items = WalletItem.objects.filter(wallet_name=req_wallet,item_type=req_item_type)
        return items


class WalletItemDetailSearchViewSet(generics.ListAPIView):
    queryset = WalletItem.objects.all()
    serializer_class = WalletItemSerializer
    # the next line is for DRF tokens, comment out for JWT tokens
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # the next line is for JWT tokens, comment out for DRF tokens
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg_1 = "wallet_name"
    lookup_url_kwarg_2 = "item_type"
    lookup_url_kwarg_3 = "item_id"

    def get_queryset(self):
        req_wallet = self.kwargs.get(self.lookup_url_kwarg_1)
        req_item_type = self.kwargs.get(self.lookup_url_kwarg_2)
        req_item_id = self.kwargs.get(self.lookup_url_kwarg_3)
        items = WalletItem.objects.filter(wallet_name=req_wallet,item_type=req_item_type,item_id=req_item_id)
        return items


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # the next line is for JWT tokens, comment out for DRF tokens
    permission_classes = (permissions.IsAuthenticated,)

