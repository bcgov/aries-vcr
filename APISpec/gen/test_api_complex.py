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
from django.test import TestCase
from django.test import Client
import django

from rest_framework.test import APIRequestFactory
from rest_framework.parsers import JSONParser
from rest_framework import status

from . import fakedata
from .models.CurrentUserViewModel import CurrentUserViewModel
from .serializers import CurrentUserViewModelSerializer
from .models.DoingBusinessAs import DoingBusinessAs
from .serializers import DoingBusinessAsSerializer
from .models.InactiveClaimReason import InactiveClaimReason
from .serializers import InactiveClaimReasonSerializer
from .models.IssuerService import IssuerService
from .serializers import IssuerServiceSerializer
from .models.Jurisdiction import Jurisdiction
from .serializers import JurisdictionSerializer
from .models.Location import Location
from .serializers import LocationSerializer
from .models.LocationOrg import LocationOrg
from .serializers import LocationOrgSerializer
from .models.LocationType import LocationType
from .serializers import LocationTypeSerializer
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
from .models.VerifiableClaim import VerifiableClaim
from .serializers import VerifiableClaimSerializer
from .models.VerifiableClaimType import VerifiableClaimType
from .serializers import VerifiableClaimTypeSerializer
from .models.VerifiableOrg import VerifiableOrg
from .serializers import VerifiableOrgSerializer
from .models.VerifiableOrgType import VerifiableOrgType
from .serializers import VerifiableOrgTypeSerializer


# Complex API test cases. 
# If an API operation contains generated code and requires a complex model object
# (containing child items) then it is tested in this file.
#
# This file will have to be edited by hand.
class Test_Api_Complex(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()


    def test_doingbusinessasBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.DoingBusinessAsTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/doingbusinessas/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_doingbusinessasGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/doingbusinessas"
        # Create:
        serializer_class = DoingBusinessAsSerializer
        payload = fakedata.DoingBusinessAsTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_doingbusinessasIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/doingbusinessas/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.DoingBusinessAsTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_doingbusinessasIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/doingbusinessas/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.DoingBusinessAsTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.DoingBusinessAsTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_issuerservicesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/issuerservices/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_issuerservicesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/issuerservices"
        # Create:
        serializer_class = IssuerServiceSerializer
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_issuerservicesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/issuerservices/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_issuerservicesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/issuerservices/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.IssuerServiceTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
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
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_locationsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.LocationTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/locations/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_locationsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/locations"
        # Create:
        serializer_class = LocationSerializer
        payload = fakedata.LocationTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_locationsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/locations/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.LocationTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_locationsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/locations/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.LocationTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.LocationTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_rolepermissionsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/rolepermissions/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_rolepermissionsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/rolepermissions"
        # Create:
        serializer_class = RolePermissionSerializer
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_rolepermissionsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/rolepermissions/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_rolepermissionsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/rolepermissions/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.RolePermissionTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
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
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_userrolesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/userroles/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_userrolesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/userroles"
        # Create:
        serializer_class = UserRoleSerializer
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_userrolesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/userroles/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_userrolesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/userroles/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.UserRoleTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
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
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableclaimsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VerifiableClaimTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/verifiableclaims/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_verifiableclaimsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/verifiableclaims"
        # Create:
        serializer_class = VerifiableClaimSerializer
        payload = fakedata.VerifiableClaimTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableclaimsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiableclaims/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VerifiableClaimTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableclaimsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiableclaims/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VerifiableClaimTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VerifiableClaimTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableclaimtypesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VerifiableClaimTypeTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/verifiableclaimtypes/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_verifiableclaimtypesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/verifiableclaimtypes"
        # Create:
        serializer_class = VerifiableClaimTypeSerializer
        payload = fakedata.VerifiableClaimTypeTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableclaimtypesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiableclaimtypes/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VerifiableClaimTypeTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableclaimtypesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiableclaimtypes/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VerifiableClaimTypeTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VerifiableClaimTypeTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableorgsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VerifiableOrgTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/verifiableorgs/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_verifiableorgsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/verifiableorgs"
        # Create:
        serializer_class = VerifiableOrgSerializer
        payload = fakedata.VerifiableOrgTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(testUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # List:
        response = self.client.get(testUrl)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = testUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableorgsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiableorgs/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VerifiableOrgTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        deleteUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiableorgsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiableorgs/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VerifiableOrgTestDataCreate()
        jsonString = json.dumps(payload)
        response = self.client.post(createUrl, content_type='application/json', data=jsonString)
        # Check that the response is OK.
        assert status.HTTP_201_CREATED == response.status_code
        # parse the response.
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        createdId = data['id']
        # Update the object:
        updateUrl = testUrl.replace ("(?P<id>[0-9]+)",str(createdId))
        payload = fakedata.VerifiableOrgTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

if __name__ == '__main__':
    unittest.main()




