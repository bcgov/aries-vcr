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


def IssuerOrgTestDataCreate():
  return {
    'name':'Initial',
    'issuerOrgTLA':'Initial',
    'issuerOrgURL':'Initial',
    'DID':'Initial',
  }

def IssuerOrgTestDataUpdate():
  return {
    'name':'Changed',
    'issuerOrgTLA':'Changed',
    'issuerOrgURL':'Changed',
    'DID':'Changed',
  }


def JurisdictionTestDataCreate():
  return {
    'jurisdictionAbbrv':'Initial',
    'jurisdictionName':'Initial',
    'displayOrder':1,
    'isOnCommonList':True,
  }

def JurisdictionTestDataUpdate():
  return {
    'jurisdictionAbbrv':'Changed',
    'jurisdictionName':'Changed',
    'displayOrder':0,
    'isOnCommonList':False,
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
    'claimSchemaDefinition':'Initial',
  }

def VOClaimTypeTestDataUpdate():
  return {
    'theType':'Changed',
    'base64Logo':'Changed',
    'issuerURL':'Changed',
    'claimSchemaDefinition':'Changed',
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
    'Addressee':'Initial',
    'AddlDeliveryInfo':'Initial',
    'unitNumber':'Initial',
    'streetAddress':'Initial',
    'municipality':'Initial',
    'province':'Initial',
    'postalCode':'Initial',
    'latLong':'Initial',
  }

def VOLocationTestDataUpdate():
  return {
    'Addressee':'Changed',
    'AddlDeliveryInfo':'Changed',
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

