from rest_framework import serializers
from api.models import WalletItem
from django.contrib.auth.models import User


class WalletItemSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = WalletItem
        fields = ('url', 'id',
                  'created', 'wallet_name', 'item_type', 'item_id', 'item_value',
                  'creator')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'api', 'wallet_items')


