from rest_framework.serializers import (
    BooleanField,
    ModelSerializer,
    SerializerMethodField,
)

from api.v2 import utils
from api.v2.models.Address import Address
from api.v2.models.Attribute import Attribute
from api.v2.models.Claim import Claim
from api.v2.models.Credential import Credential
from api.v2.models.CredentialSet import CredentialSet
from api.v2.models.CredentialType import CredentialType
from api.v2.models.Issuer import Issuer
from api.v2.models.Name import Name
from api.v2.models.Schema import Schema
from api.v2.models.Topic import Topic
from api.v2.models.TopicRelationship import TopicRelationship


class IssuerSerializer(ModelSerializer):
    has_logo = BooleanField(source="get_has_logo", read_only=True)

    class Meta:
        model = Issuer
        exclude = ("logo_b64",)


class SchemaSerializer(ModelSerializer):
    class Meta:
        model = Schema
        fields = "__all__"


class CredentialSetSerializer(ModelSerializer):
    class Meta:
        model = CredentialSet
        fields = (
            "id",
            "create_timestamp",
            "update_timestamp",
            "latest_credential_id",
            "topic_id",
            "first_effective_date",
            "last_effective_date",
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
        )


class CredentialTypeExtSerializer(CredentialTypeSerializer):
    class Meta:
        model = CredentialType
        depth = 1
        exclude = ("logo_b64",)


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = list(
            utils.fetch_custom_settings("serializers", "Topic", "includeFields")
        )
        read_only_fields = fields


class TopicRelationshipSerializer(ModelSerializer):
    class Meta:
        model = TopicRelationship
        fields = list(
            utils.fetch_custom_settings(
                "serializers", "TopicRelationship", "includeFields"
            )
        )
        read_only_fields = fields


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = list(
            utils.fetch_custom_settings("serializers", "Address", "includeFields")
        )
        read_only_fields = fields


class ClaimSerializer(ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"


class NameSerializer(ModelSerializer):
    class Meta:
        model = Name
        fields = "__all__"


class AttributeSerializer(ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"


class CredentialAttributeSerializer(AttributeSerializer):
    class Meta(AttributeSerializer.Meta):
        fields = ("id", "type", "format", "value", "credential_id")
        read_only_fields = fields


class CredentialSerializer(ModelSerializer):
    attributes = CredentialAttributeSerializer(source="all_attributes", many=True)

    class Meta:
        model = Credential
        fields = (
            "topic",
            "credential_set",
            "credential_type",
            "credential_id",
            "credential_def_id",
            "cardinality_hash",
            "effective_date",
            "inactive",
            "latest",
            "revoked",
            "revoked_date",
            "revoked_by",
            "related_topics",
            "attributes",
            "raw_data",
        )
        read_only_fields = fields


class CredentialAddressSerializer(AddressSerializer):
    class Meta(AddressSerializer.Meta):
        fields = tuple(
            {*AddressSerializer.Meta.fields, "credential_id"} - {"credential"}
        )
        read_only_fields = fields


class CredentialNameSerializer(NameSerializer):
    class Meta(NameSerializer.Meta):
        fields = ("id", "text", "language", "credential_id", "type")
        read_only_fields = fields


class CredentialTopicSerializer(TopicSerializer):
    class Meta(TopicSerializer.Meta):
        fields = ("id", "create_timestamp", "update_timestamp", "source_id", "type")
        read_only_fields = fields


class CredentialNamedTopicSerializer(CredentialTopicSerializer):
    names = CredentialNameSerializer(source="get_active_names", many=True)
    local_name = CredentialNameSerializer(source="get_local_name")
    remote_name = CredentialNameSerializer(source="get_remote_name")

    class Meta(CredentialTopicSerializer.Meta):
        fields = CredentialTopicSerializer.Meta.fields + (
            "names",
            "local_name",
            "remote_name",
        )
        read_only_fields = fields


class TopicAttributeSerializer(AttributeSerializer):
    credential_type_id = SerializerMethodField()

    class Meta(CredentialAttributeSerializer.Meta):
        fields = (
            "id",
            "type",
            "format",
            "value",
            "credential_id",
            "credential_type_id",
        )
        read_only_fields = fields

    def get_credential_type_id(self, obj):
        return obj.credential.credential_type_id


class CredentialTopicExtSerializer(CredentialNamedTopicSerializer):
    addresses = CredentialAddressSerializer(source="get_active_addresses", many=True)
    attributes = TopicAttributeSerializer(source="get_active_attributes", many=True)

    class Meta(CredentialNamedTopicSerializer.Meta):
        fields = CredentialNamedTopicSerializer.Meta.fields + (
            "addresses",
            "attributes",
        )
        read_only_fields = fields


class CredentialExtSerializer(CredentialSerializer):
    addresses = CredentialAddressSerializer(many=True)
    attributes = CredentialAttributeSerializer(many=True)
    credential_type = CredentialTypeSerializer()
    names = CredentialNameSerializer(many=True)
    local_name = CredentialNameSerializer(source="get_local_name")
    remote_name = CredentialNameSerializer(source="get_remote_name")
    topic = CredentialTopicExtSerializer()
    related_topics = CredentialNamedTopicSerializer(many=True)

    class Meta(CredentialSerializer.Meta):
        depth = 1
        fields = (
            "id",
            "create_timestamp",
            "effective_date",
            "inactive",
            "latest",
            "revoked",
            "revoked_date",
            "credential_id",
            "credential_type",
            "addresses",
            "attributes",
            "names",
            "local_name",
            "remote_name",
            "topic",
            "related_topics",
            "raw_data",
        )
        read_only_fields = fields


class ExpandedCredentialSetSerializer(CredentialSetSerializer):
    credentials = CredentialExtSerializer(many=True)

    class Meta(CredentialSetSerializer.Meta):
        # fields = CredentialSetSerializer.Meta.fields
        fields = CredentialSetSerializer.Meta.fields + ("credentials",)
        read_only_fields = fields


class ExpandedCredentialSerializer(CredentialExtSerializer):
    credential_set = ExpandedCredentialSetSerializer()

    class Meta(CredentialExtSerializer.Meta):
        fields = CredentialExtSerializer.Meta.fields + ("credential_set",)
        read_only_fields = fields
