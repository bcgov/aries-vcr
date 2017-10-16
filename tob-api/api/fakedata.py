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

# edit this file with appropriate test data.


def CurrentUserViewModelTestDataCreate():
  return {
    'givenName':'Initial',
    'surname':'Initial',
    'email':'Initial',
    'active':True,
    'smUserId':'Initial',
    'smAuthorizationDirectory':'Initial',
  }

def CurrentUserViewModelTestDataUpdate():
  return {
    'givenName':'Changed',
    'surname':'Changed',
    'email':'Changed',
    'active':False,
    'smUserId':'Changed',
    'smAuthorizationDirectory':'Changed',
  }


def InactiveClaimReasonTestDataCreate():
  return {
    'shortReason':'Initial',
    'reason':'Initial',
    'displayOrder':1,
  }

def InactiveClaimReasonTestDataUpdate():
  return {
    'shortReason':'Changed',
    'reason':'Changed',
    'displayOrder':0,
  }


def IssuerServiceTestDataCreate():
  return {
    'name':'Initial',
    'issuerOrgTLA':'Initial',
    'issuerOrgURL':'Initial',
    'DID':'Initial',
  }

def IssuerServiceTestDataUpdate():
  return {
    'name':'Changed',
    'issuerOrgTLA':'Changed',
    'issuerOrgURL':'Changed',
    'DID':'Changed',
  }


def JurisdictionTestDataCreate():
  return {
    'abbrv':'Initial',
    'name':'Initial',
    'displayOrder':1,
    'isOnCommonList':True,
  }

def JurisdictionTestDataUpdate():
  return {
    'abbrv':'Changed',
    'name':'Changed',
    'displayOrder':0,
    'isOnCommonList':False,
  }


def PermissionTestDataCreate():
  return {
    'code':'Initial',
    'name':'Initial',
    'description':'Initial',
  }

def PermissionTestDataUpdate():
  return {
    'code':'Changed',
    'name':'Changed',
    'description':'Changed',
  }


def PermissionViewModelTestDataCreate():
  return {
    'code':'Initial',
    'name':'Initial',
    'description':'Initial',
  }

def PermissionViewModelTestDataUpdate():
  return {
    'code':'Changed',
    'name':'Changed',
    'description':'Changed',
  }


def RoleTestDataCreate():
  return {
    'name':'Initial',
    'description':'Initial',
  }

def RoleTestDataUpdate():
  return {
    'name':'Changed',
    'description':'Changed',
  }


def RolePermissionTestDataCreate():
  return {
  }

def RolePermissionTestDataUpdate():
  return {
  }


def RolePermissionViewModelTestDataCreate():
  return {
    'roleId':1,
    'permissionId':1,
  }

def RolePermissionViewModelTestDataUpdate():
  return {
    'roleId':0,
    'permissionId':0,
  }


def RoleViewModelTestDataCreate():
  return {
    'name':'Initial',
    'description':'Initial',
  }

def RoleViewModelTestDataUpdate():
  return {
    'name':'Changed',
    'description':'Changed',
  }


def UserTestDataCreate():
  return {
    'givenName':'Initial',
    'surname':'Initial',
    'email':'Initial',
    'userId':'Initial',
    'guid':'Initial',
    'authorizationDirectory':'Initial',
  }

def UserTestDataUpdate():
  return {
    'givenName':'Changed',
    'surname':'Changed',
    'email':'Changed',
    'userId':'Changed',
    'guid':'Changed',
    'authorizationDirectory':'Changed',
  }


def UserDetailsViewModelTestDataCreate():
  return {
    'givenName':'Initial',
    'surname':'Initial',
    'email':'Initial',
    'active':True,
  }

def UserDetailsViewModelTestDataUpdate():
  return {
    'givenName':'Changed',
    'surname':'Changed',
    'email':'Changed',
    'active':False,
  }


def UserRoleTestDataCreate():
  return {
  }

def UserRoleTestDataUpdate():
  return {
  }


def UserRoleViewModelTestDataCreate():
  return {
    'roleId':1,
    'userId':1,
  }

def UserRoleViewModelTestDataUpdate():
  return {
    'roleId':0,
    'userId':0,
  }


def UserViewModelTestDataCreate():
  return {
    'givenName':'Initial',
    'surname':'Initial',
    'email':'Initial',
    'active':True,
    'smUserId':'Initial',
  }

def UserViewModelTestDataUpdate():
  return {
    'givenName':'Changed',
    'surname':'Changed',
    'email':'Changed',
    'active':False,
    'smUserId':'Changed',
  }


def VOClaimTestDataCreate():
  return {
    'claimJSON':'Initial',
  }

def VOClaimTestDataUpdate():
  return {
    'claimJSON':'Changed',
  }


def VOClaimTypeTestDataCreate():
  return {
    'theType':'Initial',
    'base64Logo':'Initial',
    'issuerURL':'Initial',
  }

def VOClaimTypeTestDataUpdate():
  return {
    'theType':'Changed',
    'base64Logo':'Changed',
    'issuerURL':'Changed',
  }


def VODoingBusinessAsTestDataCreate():
  return {
    'DBA':'Initial',
  }

def VODoingBusinessAsTestDataUpdate():
  return {
    'DBA':'Changed',
  }


def VOLocationTestDataCreate():
  return {
    'addressee':'Initial',
    'addlDeliveryInfo':'Initial',
    'unitNumber':'Initial',
    'streetAddress':'Initial',
    'municipality':'Initial',
    'province':'Initial',
    'postalCode':'Initial',
    'latLong':'Initial',
  }

def VOLocationTestDataUpdate():
  return {
    'addressee':'Changed',
    'addlDeliveryInfo':'Changed',
    'unitNumber':'Changed',
    'streetAddress':'Changed',
    'municipality':'Changed',
    'province':'Changed',
    'postalCode':'Changed',
    'latLong':'Changed',
  }


def VOLocationTypeTestDataCreate():
  return {
    'theType':'Initial',
    'description':'Initial',
    'displayOrder':1,
  }

def VOLocationTypeTestDataUpdate():
  return {
    'theType':'Changed',
    'description':'Changed',
    'displayOrder':0,
  }


def VOTypeTestDataCreate():
  return {
    'theType':'Initial',
    'description':'Initial',
    'displayOrder':1,
  }

def VOTypeTestDataUpdate():
  return {
    'theType':'Changed',
    'description':'Changed',
    'displayOrder':0,
  }


def VerifiedOrgTestDataCreate():
  return {
    'busId':'Initial',
    'LegalName':'Initial',
  }

def VerifiedOrgTestDataUpdate():
  return {
    'busId':'Changed',
    'LegalName':'Changed',
  }

