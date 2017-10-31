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

from .models.CurrentUserViewModel import CurrentUserViewModel
from .models.InactiveClaimReason import InactiveClaimReason
from .models.IssuerService import IssuerService
from .models.Jurisdiction import Jurisdiction
from .models.Permission import Permission
from .models.PermissionViewModel import PermissionViewModel
from .models.Role import Role
from .models.RolePermission import RolePermission
from .models.RolePermissionViewModel import RolePermissionViewModel
from .models.RoleViewModel import RoleViewModel
from .models.User import User
from .models.UserDetailsViewModel import UserDetailsViewModel
from .models.UserRole import UserRole
from .models.UserRoleViewModel import UserRoleViewModel
from .models.UserViewModel import UserViewModel
from .models.VOClaim import VOClaim
from .models.VOClaimType import VOClaimType
from .models.VODoingBusinessAs import VODoingBusinessAs
from .models.VOLocation import VOLocation
from .models.VOLocationType import VOLocationType
from .models.VOType import VOType
from .models.VerifiedOrg import VerifiedOrg

class CurrentUserViewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = CurrentUserViewModel
    fields = ('id','givenName','surname','email','active','userRoles','smUserId','smAuthorizationDirectory')

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

class PermissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Permission
    fields = ('id','code','name','description')

class PermissionViewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = PermissionViewModel
    fields = ('id','code','name','description')

class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Role
    fields = ('id','name','description')

class RolePermissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = RolePermission
    fields = ('id','roleId','permissionId')

class RolePermissionViewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = RolePermissionViewModel
    fields = ('id','roleId','permissionId')

class RoleViewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = RoleViewModel
    fields = ('id','name','description')

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id','givenName','surname','email','userId','guid','authorizationDirectory','effectiveDate','endDate')

class UserDetailsViewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserDetailsViewModel
    fields = ('id','givenName','surname','email','active','permissions')

class UserRoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserRole
    fields = ('id','userId','roleId','effectiveDate','endDate')

class UserRoleViewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserRoleViewModel
    fields = ('id','effectiveDate','expiryDate','roleId','userId')

class UserViewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserViewModel
    fields = ('id','givenName','surname','email','active','smUserId','userRoles')

class VOClaimSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOClaim
    fields = ('id','verifiedOrgId','voClaimType','claimJSON','effectiveDate','endDate','inactiveClaimReasonId')

class VOClaimTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOClaimType
    fields = ('id','theType','base64Logo','issuerOrgId','issuerURL','effectiveDate','endDate')

class VODoingBusinessAsSerializer(serializers.ModelSerializer):
  class Meta:
    model = VODoingBusinessAs
    fields = ('id','verifiedOrgId','DBA','effectiveDate','endDate')

class VOLocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOLocation
    fields = ('id','verifiedOrgId','voLocationTypeId','addressee','addlDeliveryInfo','unitNumber','streetAddress','municipality','province','postalCode','latLong','effectiveDate','endDate')

class VOLocationTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOLocationType
    fields = ('id','theType','description','effectiveDate','endDate','displayOrder')

class VOTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = VOType
    fields = ('id','theType','description','effectiveDate','endDate','displayOrder')

class VerifiedOrgSerializer(serializers.ModelSerializer):
  class Meta:
    model = VerifiedOrg
    fields = ('id','busId','orgTypeId','jurisdictionId','LegalName','effectiveDate','endDate')

class VerifiedOrgDetailSerializer(serializers.ModelSerializer):
  locations = VOLocationSerializer(many=True, read_only=True)
  claims = VOClaimSerializer(many=True, read_only=True)
  doingBusinessAs = VODoingBusinessAsSerializer(many=True, read_only=True)
  
  class Meta:
    model = VerifiedOrg
    fields = ('id','busId','orgTypeId','jurisdictionId','LegalName','effectiveDate','endDate','claims','doingBusinessAs','locations')
