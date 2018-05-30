from rest_framework.serializers import ModelSerializer
from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.models.CredentialType import CredentialType


class IssuerSerializer(ModelSerializer):
    class Meta:
        model = Issuer
        fields = "__all__"


class SchemaSerializer(ModelSerializer):
    class Meta:
        model = Schema
        fields = "__all__"


class CredentialTypeSerializer(ModelSerializer):
    class Meta:
        model = CredentialType
        fields = "__all__"
