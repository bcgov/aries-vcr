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
    "givenName":"Initial",
    "surname":"Initial",
    "email":"Initial",
    "active":True,
    "smUserId":"Initial",
    "smAuthorizationDirectory":"Initial",
  }

def CurrentUserViewModelTestDataUpdate():
  return {
    "givenName":"Changed",
    "surname":"Changed",
    "email":"Changed",
    "active":False,
    "smUserId":"Changed",
    "smAuthorizationDirectory":"Changed",
  }

def InactiveClaimReasonTestDataCreate():
  return {
    "displayOrder": "1",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "reason": "Claim has Expired",
    "shortReason": "Expired"
  }

def InactiveClaimReasonTestDataUpdate():
  return {
    "shortReason":"Changed",
    "reason":"Changed",
    "displayOrder":0,
  }


def IssuerServiceTestDataCreate():
  return {
    "DID": "did:sovrin:27F88573114C227A17684860",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "issuerOrgTLA": "BCReg",
    "issuerOrgURL": "https://bcregistries.gov.bc.ca",
    "jurisdictionId": "1",
    "name": "BC Registry"
  }

def IssuerServiceTestDataUpdate():
  return {
    "name":"Changed",
    "issuerOrgTLA":"Changed",
    "issuerOrgURL":"Changed",
    "DID":"Changed",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "jurisdictionId": "1",
  }

def JurisdictionTestDataCreate():
  return {
    "abbrv": "BC",
    "displayOrder": "1",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "isOnCommonList": True,
    "name": "British Columbia"
  }

def JurisdictionTestDataUpdate():
  return {
    "abbrv":"Changed",
    "name":"Changed",
    "displayOrder":0,
    "isOnCommonList":False,
  }


def PermissionTestDataCreate():
  return {
    "code":"Initial",
    "name":"Initial",
    "description":"Initial",
  }

def PermissionTestDataUpdate():
  return {
    "code":"Changed",
    "name":"Changed",
    "description":"Changed",
  }


def PermissionViewModelTestDataCreate():
  return {
    "code":"Initial",
    "name":"Initial",
    "description":"Initial",
  }

def PermissionViewModelTestDataUpdate():
  return {
    "code":"Changed",
    "name":"Changed",
    "description":"Changed",
  }


def RoleTestDataCreate():
  return {
    "name":"Initial",
    "description":"Initial",
  }

def RoleTestDataUpdate():
  return {
    "name":"Changed",
    "description":"Changed",
  }


def RolePermissionTestDataCreate():
  return {
    "permissionId": "1",
    "roleId": "1"
  }

def RolePermissionTestDataUpdate():
  return {
    "permissionId": "2",
    "roleId": "2"
  }


def RolePermissionViewModelTestDataCreate():
  return {
    "roleId":1,
    "permissionId":1,
  }

def RolePermissionViewModelTestDataUpdate():
  return {
    "roleId":0,
    "permissionId":0,
  }


def RoleViewModelTestDataCreate():
  return {
    "name":"Initial",
    "description":"Initial",
  }

def RoleViewModelTestDataUpdate():
  return {
    "name":"Changed",
    "description":"Changed",
  }


def UserTestDataCreate():
  return {
    "authorizationDirectory": "IDIR",
    "effectiveDate": "2010-10-10",
    "email": "JudyHHolbert@gustr.com",
    "endDate": None,
    "givenName": "Judy",
    "guid": None,
    "surname": "Holbert",
    "userId": None
  }

def UserTestDataUpdate():
  return {
    "givenName":"Changed",
    "surname":"Changed",
    "email":"Changed",
    "userId":"Changed",
    "guid":"Changed",
    "authorizationDirectory":"Changed",
  }


def UserDetailsViewModelTestDataCreate():
  return {
    "givenName":"Initial",
    "surname":"Initial",
    "email":"Initial",
    "active":True,
  }

def UserDetailsViewModelTestDataUpdate():
  return {
    "givenName":"Changed",
    "surname":"Changed",
    "email":"Changed",
    "active":False,
  }


def UserRoleTestDataCreate():
  return {
    "effectiveDate": "2017-01-01",
    "endDate": None,
    "roleId": "2",
    "userId": "1"
  }

def UserRoleTestDataUpdate():
  return {
    "effectiveDate": "2017-02-01",
    "endDate": None,
    "roleId": "2",
    "userId": "1"
  }


def UserRoleViewModelTestDataCreate():
  return {
    "roleId":1,
    "userId":1,
  }

def UserRoleViewModelTestDataUpdate():
  return {
    "roleId":0,
    "userId":0,
  }


def UserViewModelTestDataCreate():
  return {
    "givenName":"Initial",
    "surname":"Initial",
    "email":"Initial",
    "active":True,
    "smUserId":"Initial",
  }

def UserViewModelTestDataUpdate():
  return {
    "givenName":"Changed",
    "surname":"Changed",
    "email":"Changed",
    "active":False,
    "smUserId":"Changed",
  }


def VOClaimTestDataCreate():
  return {
    "claimJSON":"Initial",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "inactiveClaimReasonId": None,
    "inactiveReason": "N/A",
    "verifiedOrgId": "1",
    "voClaimType": "1"
  }

def VOClaimTestDataUpdate():
  return {
    "claimJSON":"Changed",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "inactiveClaimReasonId": None,
    "inactiveReason": "N/A",
    "verifiedOrgId": "1",
    "voClaimType": "1"
  }


def VOClaimTypeTestDataCreate():
  return {
    "theType":"Initial",
    "base64Logo":"Initial",
    "issuerURL":"Initial",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "issuerOrgId": "1",
  }

def VOClaimTypeTestDataUpdate():
  return {
    "theType":"Changed",
    "base64Logo":"Changed",
    "issuerURL":"Changed",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "issuerOrgId": "1",
  }

def VODoingBusinessAsTestDataCreate():
  return {
    "DBA":"Initial",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "verifiedOrgId": "2"
  }

def VODoingBusinessAsTestDataUpdate():
  return {
    "DBA":"Changed",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "verifiedOrgId": "2"
  }

def VOLocationTestDataCreate():
  return {
    "addlDeliveryInfo": None,
    "addressee": "The Original House of Pies",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "latLong": "48.343285, -123.398304",
    "municipality": "Victoria",
    "postalCode": "V8Z 2J8",
    "province": "BC",
    "streetAddress": "2262 Burdett Avenue",
    "unitNumber": None,
    "verifiedOrgId": "1",
    "voLocationTypeId": "1"
  }

def VOLocationTestDataUpdate():
  return {
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "verifiedOrgId": "1",
    "voLocationTypeId": "1",
    "addressee":"Changed",
    "addlDeliveryInfo":"Changed",
    "unitNumber":"Changed",
    "streetAddress":"Changed",
    "municipality":"Changed",
    "province":"Changed",
    "postalCode":"Changed",
    "latLong":"Changed",
  }


def VOLocationTypeTestDataCreate():
  return {
    "description": "Headquarters",
    "displayOrder": "1",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "theType": "Headquarters"
  }

def VOLocationTypeTestDataUpdate():
  return {
    "theType":"Changed",
    "description":"Changed",
    "displayOrder":0,
  }


def VOTypeTestDataCreate():
  return {
    "description": "A Registered Corporation",
    "displayOrder": "1",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "theType": "Corporation"
  }

def VOTypeTestDataUpdate():
  return {
    "theType":"Changed",
    "description":"Changed",
    "displayOrder":0,
  }


def VerifiedOrgTestDataCreate():
  return {
    "LegalName": "The Original House of Pies",
    "busId": "11121398",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "jurisdictionId": "1",
    "orgTypeId": "2"
  }

def VerifiedOrgTestDataUpdate():
  return {
    "busId":"Changed",
    "LegalName":"Changed",
    "effectiveDate": "2010-10-10",
    "endDate": None,
    "jurisdictionId": "1",
    "orgTypeId": "2"
  }

