from rest_framework.serializers import ModelSerializer
from api_v2.models import Issuer, Schema, CredentialType, Topic, Credential, Address, Claim, Contact, Name, Person


class IssuerSerializer(ModelSerializer):

    class Meta:
        model = Issuer
        fields = '__all__'


class SchemaSerializer(ModelSerializer):

    class Meta:
        model = Schema
        fields = '__all__'


class CredentialTypeSerializer(ModelSerializer):

    class Meta:
        model = CredentialType
        fields = '__all__'


class TopicSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'


class CredentialSerializer(ModelSerializer):

    class Meta:
        model = Credential
        fields = '__all__'


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class ClaimSerializer(ModelSerializer):

    class Meta:
        model = Claim
        fields = '__all__'


class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class NameSerializer(ModelSerializer):

    class Meta:
        model = Name
        fields = '__all__'


class PersonSerializer(ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'
