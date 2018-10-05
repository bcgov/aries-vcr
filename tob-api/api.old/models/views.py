from rest_framework.viewsets import ModelViewSet
from api.serializers import UserSerializer, VerifiableOrgTypeSerializer, JurisdictionSerializer, VerifiableOrgSerializer, DoingBusinessAsSerializer, InactiveClaimReasonSerializer, IssuerServiceSerializer, LocationTypeSerializer, LocationSerializer, VerifiableClaimTypeSerializer, VerifiableClaimSerializer
from api.models import User, VerifiableOrgType, Jurisdiction, VerifiableOrg, DoingBusinessAs, InactiveClaimReason, IssuerService, LocationType, Location, VerifiableClaimType, VerifiableClaim


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VerifiableOrgTypeViewSet(ModelViewSet):
    queryset = VerifiableOrgType.objects.all()
    serializer_class = VerifiableOrgTypeSerializer


class JurisdictionViewSet(ModelViewSet):
    queryset = Jurisdiction.objects.all()
    serializer_class = JurisdictionSerializer


class VerifiableOrgViewSet(ModelViewSet):
    queryset = VerifiableOrg.objects.all()
    serializer_class = VerifiableOrgSerializer


class DoingBusinessAsViewSet(ModelViewSet):
    queryset = DoingBusinessAs.objects.all()
    serializer_class = DoingBusinessAsSerializer


class InactiveClaimReasonViewSet(ModelViewSet):
    queryset = InactiveClaimReason.objects.all()
    serializer_class = InactiveClaimReasonSerializer


class IssuerServiceViewSet(ModelViewSet):
    queryset = IssuerService.objects.all()
    serializer_class = IssuerServiceSerializer


class LocationTypeViewSet(ModelViewSet):
    queryset = LocationType.objects.all()
    serializer_class = LocationTypeSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class VerifiableClaimTypeViewSet(ModelViewSet):
    queryset = VerifiableClaimType.objects.all()
    serializer_class = VerifiableClaimTypeSerializer


class VerifiableClaimViewSet(ModelViewSet):
    queryset = VerifiableClaim.objects.all()
    serializer_class = VerifiableClaimSerializer
