from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils import timezone

from datetime import datetime, date, timedelta
import pytz
import random
from string import ascii_lowercase, digits

from api_v2.models.User import User
from api_v2.models.Subscription import Subscription
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Schema import Schema
from api_v2.auth import generate_random_username


SUBSCRIBERS_GROUP_NAME = "subscriber"

def get_subscribers_group():
    group, created = Group.objects.get_or_create(name=SUBSCRIBERS_GROUP_NAME)
    return group

def get_random_password():
    return "".join([random.choice(ascii_lowercase+digits) for i in range(32)])

def get_password_expiry():
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    return now + timedelta(days=90)

class RegistrationSerializer(serializers.Serializer):
    org_name = serializers.CharField(required=True, max_length=240)
    email = serializers.CharField(required=True, max_length=128)
    target_url = serializers.CharField(required=False, max_length=240)
    hook_token = serializers.CharField(required=False, max_length=240)
    username = serializers.CharField(required=False, max_length=40)
    password = serializers.CharField(required=True, max_length=40, write_only=True)
    registration_expiry = serializers.DateTimeField(required=False, read_only=True)

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

        # TODO must populate unique DID due to database constraints
        validated_data['DID'] = "not:a:did:" + self.username

        # TODO generate password (?) for now user must supply
        #tmp_password = get_random_password()
        #validated_data['password'] = tmp_password
        validated_data['registration_expiry'] = get_password_expiry()

        print("Create user with", validated_data['username'], validated_data['password'])

        user = get_user_model().objects.create_user(**validated_data)

        user.groups.add(get_subscribers_group())
        user.save()

        #validated_data['gen_password'] = tmp_password

        return user


    def update(self, instance, validated_data):
        """
        Update and return an existing instance, given the validated data.
        """
        instance.org_name = validated_data.get('org_name', instance.org_name)
        instance.email = validated_data.get('email', instance.email)
        instance.target_url = validated_data.get('target_url', instance.target_url)
        instance.hook_token = validated_data.get('hook_token', instance.hook_token)

        # TODO potentially update password on each update?
        #instance['password'] = get_random_password()
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
            validated_data['registration_expiry'] = get_password_expiry()

        instance.save()
        return instance


class SubscriptionSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source='owner.username')
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
        owner = request.user
        validated_data['owner'] = owner
        credential_type = CredentialType.objects.filter(schema__name=validated_data['credential_type']).first()
        validated_data['credential_type'] = credential_type
        return Subscription.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing instance, given the validated data.
        """
        # TODO 
        pass


class SubscriptionResponseSerializer(SubscriptionSerializer):
    owner = RegistrationSerializer()


class RegistrationResponseSerializer(RegistrationSerializer):
    subscriptions = SubscriptionSerializer(many=True)

