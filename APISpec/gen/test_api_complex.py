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

from rest_framework.test import APIRequestFactory
from rest_framework.parsers import JSONParser
from rest_framework import status

from . import fakedata
from .models.InactiveClaimReason import InactiveClaimReason
from .serializers import InactiveClaimReasonSerializer
from .models.IssuerOrg import IssuerOrg
from .serializers import IssuerOrgSerializer
from .models.Jurisdiction import Jurisdiction
from .serializers import JurisdictionSerializer
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

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()


    def test_issuerOrgsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.IssuerOrgTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/issuerOrgs/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_issuerOrgsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/issuerOrgs"
        # Create:
        serializer_class = IssuerOrgSerializer
        payload = fakedata.IssuerOrgTestDataCreate()
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
        

    def test_issuerOrgsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/issuerOrgs/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.IssuerOrgTestDataCreate()
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
        

    def test_issuerOrgsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/issuerOrgs/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.IssuerOrgTestDataCreate()
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
        payload = fakedata.IssuerOrgTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_voClaimsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOClaimTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/voClaims/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_voClaimsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voClaims"
        # Create:
        serializer_class = VOClaimSerializer
        payload = fakedata.VOClaimTestDataCreate()
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
        

    def test_voClaimsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voClaims/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOClaimTestDataCreate()
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
        

    def test_voClaimsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voClaims/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOClaimTestDataCreate()
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
        payload = fakedata.VOClaimTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_voClaimTypesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOClaimTypeTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/voClaimTypes/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_voClaimTypesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voClaimTypes"
        # Create:
        serializer_class = VOClaimTypeSerializer
        payload = fakedata.VOClaimTypeTestDataCreate()
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
        

    def test_voClaimTypesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voClaimTypes/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOClaimTypeTestDataCreate()
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
        

    def test_voClaimTypesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voClaimTypes/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOClaimTypeTestDataCreate()
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
        payload = fakedata.VOClaimTypeTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_voLocationsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOLocationTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/voLocations/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_voLocationsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voLocations"
        # Create:
        serializer_class = VOLocationSerializer
        payload = fakedata.VOLocationTestDataCreate()
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
        

    def test_voLocationsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voLocations/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOLocationTestDataCreate()
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
        

    def test_voLocationsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voLocations/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOLocationTestDataCreate()
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
        payload = fakedata.VOLocationTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_verifiedOrgsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VerifiedOrgTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/verifiedOrgs/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_verifiedOrgsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/verifiedOrgs"
        # Create:
        serializer_class = VerifiedOrgSerializer
        payload = fakedata.VerifiedOrgTestDataCreate()
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
        

    def test_verifiedOrgsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiedOrgs/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VerifiedOrgTestDataCreate()
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
        

    def test_verifiedOrgsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/verifiedOrgs/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VerifiedOrgTestDataCreate()
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
        payload = fakedata.VerifiedOrgTestDataUpdate()
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




