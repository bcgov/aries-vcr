from rest_framework import serializers

from api_v2.models.User import User
from api_v2.models.Subscription import Subscription
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Schema import Schema
from api_v2.auth import generate_random_username


class NewRegistrationSerializer(serializers.Serializer):
    org_name = serializers.CharField(required=True, max_length=240)
    email = serializers.CharField(required=True, max_length=128)
    target_url = serializers.CharField(required=False, max_length=240)
    hook_token = serializers.CharField(required=False, max_length=240)

    def create(self, validated_data):
        """
        Create and return a new instance, given the validated data.
        """
        if 'username' in validated_data and 0 < len(validated_data['username']):
            prefix = validated_data['username'][:16] + "-"
        else:
            prefix = "hook-"
        username = generate_random_username(
                length=32, prefix=prefix, split=None
            )
        return User.objects.create(**validated_data)


class RegistrationSerializer(serializers.Serializer):
    org_name = serializers.CharField(required=True, max_length=240)
    email = serializers.CharField(required=True, max_length=128)
    target_url = serializers.CharField(required=False, max_length=240)
    hook_token = serializers.CharField(required=False, max_length=240)
    username = serializers.CharField(required=False, max_length=40)

    def create(self, validated_data):
        """
        Create and return a new instance, given the validated data.
        """
        if 'username' in validated_data and 0 < len(validated_data['username']):
            prefix = validated_data['username'][:16] + "-"
        else:
            prefix = "hook-"
        self.username = generate_random_username(
                length=32, prefix=prefix, split=None
            )
        validated_data['username'] = self.username
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class SubscriptionSerializer(serializers.Serializer):
    owner = serializers.CharField(required=True, max_length=40)
    subscription_type = serializers.CharField(required=True, max_length=20)
    topic_source_id = serializers.CharField(required=False, max_length=240)
    credential_type = serializers.CharField(required=False, max_length=240)
    target_url = serializers.CharField(required=False, max_length=240)
    hook_token = serializers.CharField(required=False, max_length=240)

    def create(self, validated_data):
        """
        Create and return a new instance, given the validated data.
        """
        owner = User.objects.filter(username=validated_data['owner']).first()
        validated_data['owner'] = owner
        credential_type = CredentialType.objects.filter(schema__name=validated_data['credential_type']).first()
        validated_data['credential_type'] = credential_type
        return Subscription.objects.create(**validated_data)


class SubscriptionResponseSerializer(SubscriptionSerializer):
    owner = RegistrationSerializer()


class RegistrationResponseSerializer(RegistrationSerializer):
    subscriptions = SubscriptionSerializer(many=True)

