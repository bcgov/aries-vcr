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

# edit this file with appropriate test data.
testDataFolder = '../APISpec/TestData/'  

def BulkInactiveClaimReasonTestDataCreate():
  dataPath = testDataFolder + 'InactiveClaimReason/InactiveClaimReason_DEAC.json'
  return open(dataPath).read()

def BulkIssuerServiceTestDataCreate():
  dataPath = testDataFolder + 'IssuerService/IssuerService_ISVC.json'
  return open(dataPath).read()

def BulkJurisdictionTestDataCreate():
  dataPath = testDataFolder + 'Jurisdiction/Jurisdiction_JUR.json'
  return open(dataPath).read()

def BulkPermissionsTestDataCreate():
  dataPath = testDataFolder + 'permissions/permissions_Perms.json'
  return open(dataPath).read()

def BulkRolePermissionTestDataCreate():
  dataPath = testDataFolder + 'rolepermission/rolepermission_RP.json'
  return open(dataPath).read()

def BulkRolesTestDataCreate():
  dataPath = testDataFolder + 'roles/roles_Role.json'
  return open(dataPath).read()

def BulkUserRoleTestDataCreate():
  dataPath = testDataFolder + 'userRole/userRole_userRole.json'
  return open(dataPath).read()

def BulkUserTestDataCreate():
  dataPath = testDataFolder + 'users/users_user.json'
  return open(dataPath).read()

def BulkVerifiableOrgTestDataCreate():
  dataPath = testDataFolder + 'VerifiableOrg/VerifiableOrg_VO.json'
  return open(dataPath).read()

def BulkVerifiableClaimTestDataCreate():
  dataPath = testDataFolder + 'VerifiableClaim/VerifiableClaim_VOC.json'
  return open(dataPath).read()

def BulkVerifiableClaimTypeTestDataCreate():
  dataPath = testDataFolder + 'VerifiableClaimType/VerifiableClaimType_CT.json'
  return open(dataPath).read()

def BulkDoingBusinessAsTestDataCreate():
  dataPath = testDataFolder + 'DoingBusinessAs/DoingBusinessAs_VODBA.json'
  return open(dataPath).read()

def BulkLocationTestDataCreate():
  dataPath = testDataFolder + 'Location/Location_VOL.json'
  return open(dataPath).read()

def BulkLocationTypeTestDataCreate():
  dataPath = testDataFolder + 'LocationType/LocationType_VLT.json'
  return open(dataPath).read()

def BulkVerifiableOrgTypeTestDataCreate():
  dataPath = testDataFolder + 'VerifiableOrgType/VerifiableOrgType_VOType.json'
  return open(dataPath).read()

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

def DoingBusinessAsTestDataCreate():
  return {
    'dbaName':'Initial',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'verifiableOrgId': '2'
  }

def DoingBusinessAsTestDataUpdate():
  return {
    'dbaName':'Changed',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'verifiableOrgId': '2'
  }

def InactiveClaimReasonTestDataCreate():
  return {
    'displayOrder': '1',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'reason': 'Claim has Expired',
    'shortReason': 'Expired'
  }

def InactiveClaimReasonTestDataUpdate():
  return {
    'shortReason':'Changed',
    'reason':'Changed',
    'displayOrder':0,
  }

def IssuerServiceTestDataCreate():
  return {
    'DID': 'did:sovrin:27F88573114C227A17684860',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'issuerOrgTLA': 'BCReg',
    'issuerOrgURL': 'https://bcregistries.gov.bc.ca',
    'jurisdictionId': '1',
    'name': 'BC Registry'
  }

def IssuerServiceTestDataUpdate():
  return {
    'name':'Changed',
    'issuerOrgTLA':'Changed',
    'issuerOrgURL':'Changed',
    'DID':'Changed',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'jurisdictionId': '1',
  }


def JurisdictionTestDataCreate():
  return {
    'abbrv': 'BC',
    'displayOrder': '1',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'isOnCommonList': True,
    'name': 'British Columbia'
  }

def JurisdictionTestDataUpdate():
  return {
    'abbrv':'Changed',
    'name':'Changed',
    'displayOrder':0,
    'isOnCommonList':False,
  }

def LocationTestDataCreate():
  return {
    'addlDeliveryInfo': None,
    'addressee': 'The Original House of Pies',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'latLong': '48.343285, -123.398304',
    'municipality': 'Victoria',
    'postalCode': 'V8Z 2J8',
    'province': 'BC',
    'streetAddress': '2262 Burdett Avenue',
    'unitNumber': None,
    'verifiableOrgId': '1',
    'locationTypeId': '1'
  }

def LocationTestDataUpdate():
  return {
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'verifiableOrgId': '1',
    'locationTypeId': '1',
    'addressee':'Changed',
    'addlDeliveryInfo':'Changed',
    'unitNumber':'Changed',
    'streetAddress':'Changed',
    'municipality':'Changed',
    'province':'Changed',
    'postalCode':'Changed',
    'latLong':'Changed',
  }

def LocationTypeTestDataCreate():
  return {
    'description': 'Headquarters',
    'displayOrder': '1',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'locType': 'Headquarters'
  }

def LocationTypeTestDataUpdate():
  return {
    'locType':'Changed',
    'description':'Changed',
    'displayOrder':0,
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
    'permissionId': '1',
    'roleId': '1'
  }

def RolePermissionTestDataUpdate():
  return {
    'permissionId': '2',
    'roleId': '2'
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
    'authorizationDirectory': 'IDIR',
    'effectiveDate': '2010-10-10',
    'email': 'JudyHHolbert@gustr.com',
    'endDate': None,
    'givenName': 'Judy',
    'guid': None,
    'surname': 'Holbert',
    'userId': None
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
    'effectiveDate': '2017-01-01',
    'endDate': None,
    'roleId': '2',
    'userId': '1'
  }

def UserRoleTestDataUpdate():
  return {
    'effectiveDate': '2017-02-01',
    'endDate': None,
    'roleId': '2',
    'userId': '1'
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

def VerifiableClaimTestDataCreate():
  return {
    'claimJSON':'Initial',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'inactiveClaimReasonId': None,
    'verifiableOrgId': '1',
    'claimType': '1'
  }

def VerifiableClaimTestDataUpdate():
  return {
    'claimJSON':'Changed',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'inactiveClaimReasonId': None,
    'verifiableOrgId': '1',
    'claimType': '1'
  }

def VerifiableClaimTypeTestDataCreate():
  return {
    'claimType':'Initial',
    'base64Logo':'Initial',
    'issuerURL':'Initial',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'issuerServiceId': '1',
  }

def VerifiableClaimTypeTestDataUpdate():
  return {
    'claimType':'Changed',
    'base64Logo':'Changed',
    'issuerURL':'Changed',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'issuerServiceId': '1',
  }

def VerifiableOrgTestDataCreate():
  return {
    'legalName': 'The Original House of Pies',
    'orgId': '11121398',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'jurisdictionId': '1',
    'orgTypeId': '2'
  }

def VerifiableOrgTestDataUpdate():
  return {
    'orgId':'Changed',
    'legalName':'Changed',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'jurisdictionId': '1',
    'orgTypeId': '2'
  }

def VerifiableOrgTypeTestDataCreate():
  return {
    'description': 'A Registered Corporation',
    'displayOrder': '1',
    'effectiveDate': '2010-10-10',
    'endDate': None,
    'orgType': 'Corporation'
  }

def VerifiableOrgTypeTestDataUpdate():
  return {
    'orgType':'Changed',
    'description':'Changed',
    'displayOrder':0,
  }

def FakeClaim():
  return json.dumps({
    "claim":
    {
      "effectiveDate": ["2010-10-01", "292278025700124567423128235555255497804808729393"],
      "orgTypeId": ["CO", "5170738278"],
      "endDate": ["None", "3775483679542162997"],
      "jurisdictionId": ["Whistler", "70735759807497014749465787221675423538"],
      "LegalName": ["ASIAN JUNCTION", "5496482086721208046300713396424647182957742358275883992817284297829"],
      "busId": ["143668", "143668"]
    },
    "schema_seq_no": 6,
    "signature":
    {
      "primary_claim":
      {
        "m2": "19088367672424418326534616450484907245328296592060315329786820321794134783571",
        "a": "997176871241301330938697502270400144053172465580529299564204880231949958724572878533829555261225181168683998175299702496443602821457887209786141416410419226379086817337113659140064684469616215685192119621106677614190914795617826159087714429621399408643698730108246200982640576051719364837601464462478540913378366838846478485589318612349428775574331625521378179321634120616035978561499314006939394980347662711448934678582521517292686585407891963803135901240589681473167720120336372663057381274561433868949573685374477756424568026973565138196345445112942842037203204806356994790339339516073673215660462577833382071200",
        "e": "259344723055062059907025491480697571938277889515152306249728583105665800713306759149981690559193987143012367913206299323899696942213235956742930299877005576932406883599076397270969",
        "v": "9529027696843348992474768895627795980648754519368541225831414014122412273506978477825207858984721361212629987973575585673674980987433802655562673016036783928045836267182413114551222568596520917576222250393164322915630795756378521064729059917975554795343347229172883266797291224355078919865796389342189711453828536200549668980900421463670435350197572727369277209483826635152205866125500005591476540484002782772461901541917799894465769144232251857206978337831561796782649466849475396560690180180064902334712384826188080057840670206830243703817649516015063191764927340176438189278350618087701913735660854663957221344384791196634489941588305399778747091004977814949697295898048333134239579494256382406865858663180201635190730384111824432217493654894092246191798857614137824088942100658430953064906467212852483132037764366522"
      },
      "non_revocation_claim": None
    },
    "issuer_did": "Q4zqM7aXqm7gDQkUVLng9h"
  })