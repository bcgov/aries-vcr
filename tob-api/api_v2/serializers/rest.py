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


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = "__all__"


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
