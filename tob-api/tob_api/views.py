
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from api.models.VerifiableClaim import VerifiableClaim
from api.models.VerifiableOrg import VerifiableOrg
from api.models.InactiveClaimReason import InactiveClaimReason
from api.models.IssuerService import IssuerService
from api.models.Jurisdiction import Jurisdiction
from api.models.LocationType import LocationType
from api.models.VerifiableClaimType import VerifiableClaimType
from api.models.VerifiableOrgType import VerifiableOrgType
from api import serializers


def health(request):
    """
    Health check for OpenShift
    """
    return HttpResponse(VerifiableClaim.objects.count())


def quickload(request):
	"""
	Return record counts and data types required by the web application, all together
	"""

	response = {'counts': {}, 'records': {}}

	countOrgs = VerifiableOrg.objects.count()
	countClaims = VerifiableClaim.objects.count()
	response['counts'] = {'verifiableorgs': countOrgs, 'verifiableclaims': countClaims}

	inactive = InactiveClaimReason.objects.all()
	response['records']['inactiveclaimreasons'] = serializers.InactiveClaimReasonSerializer(inactive, many=True).data

	issuers = IssuerService.objects.all()
	response['records']['issuerservices'] = serializers.IssuerServiceSerializer(issuers, many=True).data

	jurisd = Jurisdiction.objects.all()
	response['records']['jurisdictions'] = serializers.JurisdictionSerializer(jurisd, many=True).data

	locTypes = LocationType.objects.all()
	response['records']['locationtypes'] = serializers.LocationTypeSerializer(locTypes, many=True).data

	claimTypes = VerifiableClaimType.objects.all()
	response['records']['verifiableclaimtypes'] = serializers.VerifiableClaimTypeSerializer(claimTypes, many=True).data

	orgTypes = VerifiableOrgType.objects.all()
	response['records']['verifiableorgtypes'] = serializers.VerifiableOrgTypeSerializer(orgTypes, many=True).data

	return JsonResponse(response)
