from rest_framework.serializers import ModelSerializer
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


class IssuerSerializer(ModelSerializer):
    class Meta:
        model = Issuer
        depth = 2
        fields = "__all__"


class SchemaSerializer(ModelSerializer):
    class Meta:
        model = Schema
        depth = 2
        fields = "__all__"


class CredentialTypeSerializer(ModelSerializer):
    class Meta:
        model = CredentialType
        depth = 2
        fields = "__all__"


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        depth = 2
        fields = "__all__"


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        depth = 2
        fields = "__all__"


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        depth = 2
        fields = "__all__"


class ClaimSerializer(ModelSerializer):
    class Meta:
        model = Claim
        depth = 2
        fields = "__all__"


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        depth = 2
        fields = "__all__"


class NameSerializer(ModelSerializer):
    class Meta:
        model = Name
        depth = 2
        fields = "__all__"


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        depth = 2
        fields = "__all__"
