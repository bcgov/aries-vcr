from rest_framework.serializers import (
    BooleanField,
    ModelSerializer,
)

from api.v2.models.Attribute import Attribute
from api.v2.models.Credential import Credential
from api.v2.models.CredentialType import CredentialType
from api.v2.models.Schema import Schema

from api.v2.serializers.rest import CredentialNameSerializer, IssuerSerializer


class AttributeSerializer(ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"


class CredentialAttributeSerializer(AttributeSerializer):
    class Meta(AttributeSerializer.Meta):
        ref_name = "V4CredentialAttributeSerializer"

        fields = (
            "id",
            "type",
            "format",
            "value",
        )
        read_only_fields = fields


class CredentialTypeSchemaSerializer(ModelSerializer):
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
            "highlighted_attributes",
            "credential_title",
            "issuer",
        )


class CredentialTypeExtendedSerializer(ModelSerializer):
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
        )


class SchemaSerializer(ModelSerializer):
    credential_types = CredentialTypeSchemaSerializer(many=True)

    class Meta:
        model = Schema
        fields = ("name", "origin_did", "credential_types")


class CredentialTypeClaimLabelsSerializer(ModelSerializer):
    issuer = IssuerSerializer()
    has_logo = BooleanField(source="get_has_logo", read_only=True)

    class Meta:
        model = CredentialType
        depth = 1
        exclude = (
            "category_labels",
            "claim_descriptions",
            "logo_b64",
            "processor_config",
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
    credential_type = CredentialTypeExtendedSerializer()


class RawCredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = ("raw_data",)
        read_only_fields = fields

    def to_representation(self, instance):
        return instance.raw_data or {}
