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


# Simple API test cases. 
# If an API operation contains generated code and requires a simple model object
# (one that is not complex, containing child items) then it is tested in this 
# file.
#
# See the file test_api_complex.py for other test cases, which must be hand 
# written.
class Test_Api_Simple(TestCase):
    
    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()


    def test_inactiveclaimreasonsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.InactiveClaimReasonTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/inactiveclaimreasons/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_inactiveclaimreasonsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/inactiveclaimreasons"
        # Create:
        serializer_class = InactiveClaimReasonSerializer
        payload = fakedata.InactiveClaimReasonTestDataCreate()
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
        

    def test_inactiveclaimreasonsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/inactiveclaimreasons/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.InactiveClaimReasonTestDataCreate()
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
        

    def test_inactiveclaimreasonsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/inactiveclaimreasons/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.InactiveClaimReasonTestDataCreate()
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
        payload = fakedata.InactiveClaimReasonTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_jurisdictionsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.JurisdictionTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/jurisdictions/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_jurisdictionsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/jurisdictions"
        # Create:
        serializer_class = JurisdictionSerializer
        payload = fakedata.JurisdictionTestDataCreate()
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
        

    def test_jurisdictionsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/jurisdictions/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.JurisdictionTestDataCreate()
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
        

    def test_jurisdictionsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/jurisdictions/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.JurisdictionTestDataCreate()
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
        payload = fakedata.JurisdictionTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_permissionsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.PermissionTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/permissions/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_permissionsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/permissions"
        # Create:
        serializer_class = PermissionSerializer
        payload = fakedata.PermissionTestDataCreate()
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
        

    def test_permissionsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/permissions/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.PermissionTestDataCreate()
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
        

    def test_permissionsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/permissions/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.PermissionTestDataCreate()
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
        payload = fakedata.PermissionTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_rolesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.RoleTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/roles/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_rolesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/roles"
        # Create:
        serializer_class = RoleSerializer
        payload = fakedata.RoleTestDataCreate()
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
        

    def test_rolesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/roles/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.RoleTestDataCreate()
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
        

    def test_rolesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/roles/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.RoleTestDataCreate()
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
        payload = fakedata.RoleTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_usersBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.UserTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/users/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_usersGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/users"
        # Create:
        serializer_class = UserSerializer
        payload = fakedata.UserTestDataCreate()
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
        

    def test_usersIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/users/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.UserTestDataCreate()
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
        

    def test_usersIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/users/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.UserTestDataCreate()
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
        payload = fakedata.UserTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_volocationtypesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOLocationTypeTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/volocationtypes/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_volocationtypesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/volocationtypes"
        # Create:
        serializer_class = VOLocationTypeSerializer
        payload = fakedata.VOLocationTypeTestDataCreate()
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
        

    def test_volocationtypesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/volocationtypes/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOLocationTypeTestDataCreate()
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
        

    def test_volocationtypesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/volocationtypes/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOLocationTypeTestDataCreate()
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
        payload = fakedata.VOLocationTypeTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        

    def test_voorgtypesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOTypeTestDataCreate()
        jsonString = "[" + json.dumps(payload) + "]"
        response = self.client.post('/api/v1/voorgtypes/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        

    def test_voorgtypesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voorgtypes"
        # Create:
        serializer_class = VOTypeSerializer
        payload = fakedata.VOTypeTestDataCreate()
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
        

    def test_voorgtypesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voorgtypes/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOTypeTestDataCreate()
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
        

    def test_voorgtypesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voorgtypes/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOTypeTestDataCreate()
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
        payload = fakedata.VOTypeTestDataUpdate()
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




