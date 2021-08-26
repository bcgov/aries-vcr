from rest_framework.serializers import (
    BooleanField,
    ModelSerializer,
)

from api.v2.models.Attribute import Attribute
from api.v2.models.Credential import Credential
from api.v2.models.CredentialType import CredentialType
from api.v2.models.Issuer import Issuer

from api.v2.serializers.rest import CredentialNameSerializer


class IssuerSerializer(ModelSerializer):
    has_logo = BooleanField(source="get_has_logo", read_only=True)

    class Meta:
        model = Issuer
        exclude = (
            "logo_b64",
        )


class AttributeSerializer(ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"


class CredentialAttributeSerializer(AttributeSerializer):
    class Meta(AttributeSerializer.Meta):
        fields = (
            "id",
            "type",
            "format",
            "value",
        )
        read_only_fields = fields


class CredentialTypeSerializer(ModelSerializer):
    issuer = IssuerSerializer()
    has_logo = BooleanField(source="get_has_logo", read_only=True)

    class Meta:
        model = CredentialType
        depth = 1
        exclude = (
            "category_labels",
            "claim_descriptions",
            "claim_labels",
            "logo_b64",
            "processor_config",
            "visible_fields",
            "schema",
        )


class CredentialSerializer(ModelSerializer):
    attributes = CredentialAttributeSerializer(many=True)
    names = CredentialNameSerializer(many=True)

    class Meta:
        model = Credential
        fields = (
            "id",
            "credential_type",
            "credential_id",
            "credential_def_id",
            "effective_date",
            "inactive",
            "latest",
            "revoked",
            "revoked_date",
            "revoked_by",
            "attributes",
            "names",
        )
        read_only_fields = fields


class RestSerializer(CredentialSerializer):
    credential_type = CredentialTypeSerializer()
