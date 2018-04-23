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

from rest_framework import serializers

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

class DoingBusinessAsSerializer(serializers.ModelSerializer):
  class Meta:
    model = DoingBusinessAs
    fields = ('id','verifiableOrgId','dbaName','effectiveDate','endDate')

class InactiveClaimReasonSerializer(serializers.ModelSerializer):
  class Meta:
    model = InactiveClaimReason
    fields = ('id','shortReason','reason','effectiveDate','endDate','displayOrder')

class IssuerServiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = IssuerService
    fields = ('id','name','issuerOrgTLA','issuerOrgURL','DID','jurisdictionId','effectiveDate','endDate')

class JurisdictionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Jurisdiction
    fields = ('id','abbrv','name','displayOrder','isOnCommonList','effectiveDate','endDate')

class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Location
    fields = ('id','verifiableOrgId','doingBusinessAsId','locationTypeId','addressee','addlDeliveryInfo','unitNumber','streetAddress','municipality','province','postalCode','latLong','effectiveDate','endDate')

class LocationTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = LocationType
    fields = ('id','locType','description','effectiveDate','endDate','displayOrder')

class VerifiableClaimSerializer(serializers.ModelSerializer):
  class Meta:
    model = VerifiableClaim
    fields = ('id','verifiableOrgId','claimType','claimJSON','effectiveDate','endDate','inactiveClaimReasonId')

class VerifiableClaimTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VerifiableClaimType
    fields = ('id','claimType','schemaName','schemaVersion','base64Logo','issuerServiceId','issuerURL','effectiveDate','endDate')

class VerifiableOrgSerializer(serializers.ModelSerializer):
  class Meta:
    model = VerifiableOrg
    fields = ('id','orgId','orgTypeId','jurisdictionId','legalName','effectiveDate','endDate')

class VerifiableOrgTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VerifiableOrgType
    fields = ('id','orgType','description','effectiveDate','endDate','displayOrder')

class DoingBusinessAsDetailSerializer(serializers.ModelSerializer):
  locations = LocationSerializer(many=True, read_only=True)
  class Meta:
    model = DoingBusinessAs
    fields = ('id','verifiableOrgId','dbaName','effectiveDate','endDate','locations')

class VerifiableOrgDetailSerializer(serializers.ModelSerializer):
  locations = LocationSerializer(many=True, read_only=True)
  claims = VerifiableClaimSerializer(many=True, read_only=True)
  doingBusinessAs = DoingBusinessAsDetailSerializer(many=True, read_only=True)
  class Meta:
    model = VerifiableOrg
    fields = ('id','orgId','orgTypeId','jurisdictionId','legalName','effectiveDate','endDate','claims','doingBusinessAs','locations')
