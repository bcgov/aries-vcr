"""
    REST API Documentation for TheOrgBook

    TheOrgBook is a repository for Verifiable Claims made about Organizations related to a known foundational Verifiable Claim. See https://github.com/bcgov/VON

    OpenAPI spec version: v1
        

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import json
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions 
from rest_framework import mixins
from rest_framework import generics
from rest_framework_bulk import BulkCreateModelMixin
from . import serializers
from .models.DoingBusinessAs import DoingBusinessAs
from .models.InactiveClaimReason import InactiveClaimReason
from .models.IssuerService import IssuerService
from .models.Jurisdiction import Jurisdiction
from .models.Location import Location
from .models.LocationType import LocationType
from .models.VerifiableClaim import VerifiableClaim
from .models.VerifiableClaimType import VerifiableClaimType
from .models.VerifiableOrg import VerifiableOrg
from .models.VerifiableOrgType import VerifiableOrgType

from django.db.models import Count

# Custom views.  This file is hand edited.

class verifiableOrgsIdVerifiableclaimsGet(APIView):
  def get(self, request, id):
    """  
    Returns the Claims for a verifiable Organization  
    """
    org = VerifiableOrg.objects.get(id=id)
    claims = VerifiableClaim.objects.filter(verifiableOrgId=org)
    serializer = serializers.VerifiableClaimSerializer(claims, many=True)
    return Response(serializer.data)

class verifiableOrgsIdDoingBusinessAsGet(APIView):
  def get(self, request, id):
    """  
    Returns the Doing Business As information for a verifiable Organization  
    """
    org = VerifiableOrg.objects.get(id=id)
    dbas = DoingBusinessAs.objects.filter(verifiableOrgId=org)
    serializer = serializers.DoingBusinessAsSerializer(dbas, many=True)
    return Response(serializer.data)

class verifiableOrgsIdLocationsGet(APIView):
  def get(self, request, id):
    """  
    Returns the locations for a verifiable Organization  
    """
    org = VerifiableOrg.objects.get(id=id)
    locations = Location.objects.filter(verifiableOrgId=org)
    serializer = serializers.LocationSerializer(locations, many=True)
    return Response(serializer.data)

class quickLoad(APIView):
  def get(self, request):
    """
    Used to initialize a client application.
    Returns record counts, and data types required by the web application to perform filtering and/or populate list(s).
    """
    response = {
      'counts': recordCounts.get_recordCounts(),
      'records': {}
    }

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
  
class recordCounts(APIView):
  @staticmethod
  def get_recordCounts():
    return {
      'doingbusinessas': DoingBusinessAs.objects.count(),
      'inactiveclaimreasons': InactiveClaimReason.objects.count(),
      'issuerservices': IssuerService.objects.count(),
      'jurisdictions': Jurisdiction.objects.count(),
      'locations': Location.objects.count(),
      'locationtypes': LocationType.objects.count(),
      'verifiableclaims': VerifiableClaim.objects.count(),
      'verifiableclaimtypes': VerifiableClaimType.objects.count(),
      'verifiableorgs': VerifiableOrg.objects.count(),
      'verifiableorgtypes': VerifiableOrgType.objects.count(),
    }
  
  def get(self, request):
    """  
    Returns record count information.
    """
    response = {
      'counts': self.get_recordCounts()
    }
    
    return JsonResponse(response)
