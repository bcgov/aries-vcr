"""
    REST API Documentation for TheOrgBook

    TheOrgBook is a repository for Verified Claims made about Organizations related to a known foundational Verified Claim. See https://github.com/bcgov/VON

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

from .models.InactiveClaimReason import InactiveClaimReason
from .models.IssuerOrg import IssuerOrg
from .models.Jurisdiction import Jurisdiction
from .models.VOClaim import VOClaim
from .models.VOClaimType import VOClaimType
from .models.VODoingBusinessAs import VODoingBusinessAs
from .models.VOLocation import VOLocation
from .models.VOLocationType import VOLocationType
from .models.VOType import VOType
from .models.VerifiedOrg import VerifiedOrg

class InactiveClaimReasonSerializer(serializers.ModelSerializer):
  class Meta:
    model = InactiveClaimReason
    fields = ('id','shortReason','reason','effectiveDate','expirationDate','displayOrder')

class IssuerOrgSerializer(serializers.ModelSerializer):
  class Meta:
    model = IssuerOrg
    fields = ('id','name','issuerOrgTLA','issuerOrgURL','DID','jurisdictionId','effectiveDate','expirationDate')

class JurisdictionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Jurisdiction
    fields = ('id','jurisdictionAbbrv','jurisdictionName','displayOrder','isOnCommonList','effectiveDate','expirationDate')

class VOClaimSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOClaim
    fields = ('id','verifiedOrgId','voClaimType','claimJSON','effectiveDate','endDate','inactiveClaimReasonId')

class VOClaimTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOClaimType
    fields = ('id','theType','base64Logo','issuerOrgId','issuerURL','claimSchemaDefinition')

class VODoingBusinessAsSerializer(serializers.ModelSerializer):
  class Meta:
    model = VODoingBusinessAs
    fields = ('id','DBA','effectiveDate','endDate')

class VOLocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOLocation
    fields = ('id','voLocationTypeId','Addressee','AddlDeliveryInfo','unitNumber','streetAddress','municipality','province','postalCode','latLong')

class VOLocationTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOLocationType
    fields = ('id','theType','description','effectiveDate','expirationDate','displayOrder')

class VOTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOType
    fields = ('id','theType','description','effectiveDate','expirationDate','displayOrder')

class VerifiedOrgSerializer(serializers.ModelSerializer):
  class Meta:
    model = VerifiedOrg
    fields = ('id','busId','orgType','jurisdictionId','LegalName','primaryLocation','effectiveDate','endDate')

