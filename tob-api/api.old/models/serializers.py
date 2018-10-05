from rest_framework.serializers import ModelSerializer
from api.models import User, VerifiableOrgType, Jurisdiction, VerifiableOrg, DoingBusinessAs, InactiveClaimReason, IssuerService, LocationType, Location, VerifiableClaimType, VerifiableClaim


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        depth = 2
        fields = '__all__'


class VerifiableOrgTypeSerializer(ModelSerializer):

    class Meta:
        model = VerifiableOrgType
        depth = 2
        fields = '__all__'


class JurisdictionSerializer(ModelSerializer):

    class Meta:
        model = Jurisdiction
        depth = 2
        fields = '__all__'


class VerifiableOrgSerializer(ModelSerializer):

    class Meta:
        model = VerifiableOrg
        depth = 2
        fields = '__all__'


class DoingBusinessAsSerializer(ModelSerializer):

    class Meta:
        model = DoingBusinessAs
        depth = 2
        fields = '__all__'


class InactiveClaimReasonSerializer(ModelSerializer):

    class Meta:
        model = InactiveClaimReason
        depth = 2
        fields = '__all__'


class IssuerServiceSerializer(ModelSerializer):

    class Meta:
        model = IssuerService
        depth = 2
        fields = '__all__'


class LocationTypeSerializer(ModelSerializer):

    class Meta:
        model = LocationType
        depth = 2
        fields = '__all__'


class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        depth = 2
        fields = '__all__'


class VerifiableClaimTypeSerializer(ModelSerializer):

    class Meta:
        model = VerifiableClaimType
        depth = 2
        fields = '__all__'


class VerifiableClaimSerializer(ModelSerializer):

    class Meta:
        model = VerifiableClaim
        depth = 2
        fields = '__all__'
