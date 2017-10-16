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

import json
from django.test import TestCase
from django.test import Client
import django
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework.parsers import JSONParser
from rest_framework import status

from . import fakedata
from .models.CurrentUserViewModel import CurrentUserViewModel
from .serializers import CurrentUserViewModelSerializer
from .models.InactiveClaimReason import InactiveClaimReason
from .serializers import InactiveClaimReasonSerializer
from .models.IssuerService import IssuerService
from .serializers import IssuerServiceSerializer
from .models.Jurisdiction import Jurisdiction
from .serializers import JurisdictionSerializer
from .models.Permission import Permission
from .serializers import PermissionSerializer
from .models.PermissionViewModel import PermissionViewModel
from .serializers import PermissionViewModelSerializer
from .models.Role import Role
from .serializers import RoleSerializer
from .models.RolePermission import RolePermission
from .serializers import RolePermissionSerializer
from .models.RolePermissionViewModel import RolePermissionViewModel
from .serializers import RolePermissionViewModelSerializer
from .models.RoleViewModel import RoleViewModel
from .serializers import RoleViewModelSerializer
from .models.User import User
from .serializers import UserSerializer
from .models.UserDetailsViewModel import UserDetailsViewModel
from .serializers import UserDetailsViewModelSerializer
from .models.UserRole import UserRole
from .serializers import UserRoleSerializer
from .models.UserRoleViewModel import UserRoleViewModel
from .serializers import UserRoleViewModelSerializer
from .models.UserViewModel import UserViewModel
from .serializers import UserViewModelSerializer
from .models.VOClaim import VOClaim
from .serializers import VOClaimSerializer
from .models.VOClaimType import VOClaimType
from .serializers import VOClaimTypeSerializer
from .models.VODoingBusinessAs import VODoingBusinessAs
from .serializers import VODoingBusinessAsSerializer
from .models.VOLocation import VOLocation
from .serializers import VOLocationSerializer
from .models.VOLocationType import VOLocationType
from .serializers import VOLocationTypeSerializer
from .models.VOType import VOType
from .serializers import VOTypeSerializer
from .models.VerifiedOrg import VerifiedOrg
from .serializers import VerifiedOrgSerializer


# Complex API test cases. 
# If an API operation contains generated code and requires a complex model object
# (containing child items) then it is tested in this file.
#
# This file will have to be edited by hand.
class Test_Api_Complex(TestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()


    def test_issuerservicesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/issuerservices/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_issuerservicesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/issuerservices"
        # Create:
        serializer_class = IssuerServiceSerializer
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_issuerservicesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/issuerservices/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_issuerservicesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/issuerservices/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.IssuerServiceTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_rolepermissionsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/rolepermissions/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_rolepermissionsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/rolepermissions"
        # Create:
        serializer_class = RolePermissionSerializer
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_rolepermissionsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/rolepermissions/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_rolepermissionsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/rolepermissions/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.RolePermissionTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_userrolesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/userroles/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_userrolesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/userroles"
        # Create:
        serializer_class = UserRoleSerializer
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_userrolesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/userroles/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_userrolesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/userroles/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.UserRoleTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_voclaimsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOClaimTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/voclaims/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_voclaimsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voclaims"
        # Create:
        serializer_class = VOClaimSerializer
        payload = fakedata.VOClaimTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_voclaimsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voclaims/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOClaimTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_voclaimsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voclaims/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOClaimTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VOClaimTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_voclaimtypesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOClaimTypeTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/voclaimtypes/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_voclaimtypesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voclaimtypes"
        # Create:
        serializer_class = VOClaimTypeSerializer
        payload = fakedata.VOClaimTypeTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_voclaimtypesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voclaimtypes/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOClaimTypeTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_voclaimtypesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voclaimtypes/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOClaimTypeTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VOClaimTypeTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_vodoingbusinessasBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VODoingBusinessAsTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/vodoingbusinessas/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_vodoingbusinessasGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/vodoingbusinessas"
        # Create:
        serializer_class = VODoingBusinessAsSerializer
        payload = fakedata.VODoingBusinessAsTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_vodoingbusinessasIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/vodoingbusinessas/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VODoingBusinessAsTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_vodoingbusinessasIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/vodoingbusinessas/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VODoingBusinessAsTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VODoingBusinessAsTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_volocationsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOLocationTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/volocations/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_volocationsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/volocations"
        # Create:
        serializer_class = VOLocationSerializer
        payload = fakedata.VOLocationTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_volocationsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/volocations/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOLocationTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_volocationsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/volocations/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOLocationTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VOLocationTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_verifiedorgsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VerifiedOrgTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/verifiedorgs/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_verifiedorgsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/verifiedorgs"
        # Create:
        serializer_class = VerifiedOrgSerializer
        payload = fakedata.VerifiedOrgTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_verifiedorgsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiedorgs/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VerifiedOrgTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_verifiedorgsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiedorgs/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VerifiedOrgTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VerifiedOrgTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

if __name__ == '__main__':
    unittest.main()




