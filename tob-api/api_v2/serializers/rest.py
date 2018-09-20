from rest_framework.serializers import BooleanField, ModelSerializer
from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Topic import Topic
from api_v2.models.Credential import Credential
from api_v2.models.Address import Address
from api_v2.models.Claim import Claim
from api_v2.models.Contact import Contact
from api_v2.models.Name import Name
from api_v2.models.Person import Person
from api_v2.models.Category import Category
from api_v2 import utils


class IssuerSerializer(ModelSerializer):
    has_logo = BooleanField(source="get_has_logo", read_only=True)

    class Meta:
        model = Issuer
        exclude = (
            "logo_b64",
        )


class SchemaSerializer(ModelSerializer):
    class Meta:
        model = Schema
        fields = "__all__"


class CredentialTypeSerializer(ModelSerializer):
    issuer = IssuerSerializer()
    has_logo = BooleanField(source="get_has_logo", read_only=True)

    class Meta:
        model = CredentialType
        depth = 1
        exclude = (
            "logo_b64",
            "processor_config",
            "visible_fields",
        )


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = list(utils.fetch_custom_settings('serializers', 'Topic', 'includeFields'))


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = list(utils.fetch_custom_settings('serializers', 'Address', 'includeFields'))


class ClaimSerializer(ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class NameSerializer(ModelSerializer):
    class Meta:
        model = Name
        fields = "__all__"


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = "__all__"

class CredentialAddressSerializer(AddressSerializer):
    class Meta(AddressSerializer.Meta):
        fields = tuple(
            {*AddressSerializer.Meta.fields, "credential_id"} - {"credential"}
        )

class CredentialCategorySerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = ("id", "type", "value", "credential_id")

class CredentialContactSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        fields = ("id", "type", "text", "credential_id")

class CredentialNameSerializer(NameSerializer):
    class Meta(NameSerializer.Meta):
        fields = ("id", "text", "language", "credential_id")

class CredentialPersonSerializer(PersonSerializer):
    class Meta(PersonSerializer.Meta):
        fields = ("id", "full_name", "credential_id")

class CredentialTopicSerializer(TopicSerializer):
    class Meta(TopicSerializer.Meta):
        fields = (
            "id", "create_timestamp", "update_timestamp",
            "source_id", "type",
        )


class CredentialTopicExtSerializer(TopicSerializer):
    addresses = CredentialAddressSerializer(source='get_active_addresses', many=True)
    categories = CredentialCategorySerializer(source='get_active_categories', many=True)
    #contacts = CredentialContactSerializer(source='get_active_contacts', many=True)
    names = CredentialNameSerializer(source='get_active_names', many=True)
    #people = CredentialPersonSerializer(source='get_active_people', many=True)

    class Meta(TopicSerializer.Meta):
        fields = (
            "id", "create_timestamp", "update_timestamp",
            "source_id", "type",
            "addresses", "categories", "names",
        )

class ExpandedCredentialSerializer(CredentialSerializer):
    addresses = CredentialAddressSerializer(many=True)
    categories = CredentialCategorySerializer(many=True)
    contacts = CredentialContactSerializer(many=True)
    credential_type = CredentialTypeSerializer()
    names = CredentialNameSerializer(many=True)
    people = CredentialPersonSerializer(many=True)
    topic = CredentialTopicExtSerializer()

    class Meta(CredentialSerializer.Meta):
        depth = 1
        fields = (
            "id",
            "effective_date",
            "inactive",
            "revoked",
            "wallet_id",
            "credential_type",
            "addresses",
            "categories",
            "names",
            "contacts",
            "people",
            "topic",
        )
