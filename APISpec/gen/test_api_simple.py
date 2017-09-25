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


# Simple API test cases. 
# If an API operation contains generated code and requires a simple model object
# (one that is not complex, containing child items) then it is tested in this 
# file.
#
# See the file test_api_complex.py for other test cases, which must be hand 
# written.
class Test_Api_Simple(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()


    def test_inactiveClaimReasonsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.InactiveClaimReasonTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/inactiveClaimReasons/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_inactiveClaimReasonsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/inactiveClaimReasons"
        # Create:
        serializer_class = InactiveClaimReasonSerializer
        payload = fakedata.InactiveClaimReasonTestDataCreate()
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
        

    def test_inactiveClaimReasonsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/inactiveClaimReasons/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.InactiveClaimReasonTestDataCreate()
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
        

    def test_inactiveClaimReasonsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/inactiveClaimReasons/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.InactiveClaimReasonTestDataCreate()
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
        payload = fakedata.InactiveClaimReasonTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_jurisdictionsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.JurisdictionTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/jurisdictions/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_jurisdictionsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/jurisdictions"
        # Create:
        serializer_class = JurisdictionSerializer
        payload = fakedata.JurisdictionTestDataCreate()
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
        

    def test_jurisdictionsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/jurisdictions/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.JurisdictionTestDataCreate()
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
        

    def test_jurisdictionsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/jurisdictions/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.JurisdictionTestDataCreate()
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
        payload = fakedata.JurisdictionTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_voDoingBusinessAsBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VODoingBusinessAsTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/voDoingBusinessAs/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_voDoingBusinessAsGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voDoingBusinessAs"
        # Create:
        serializer_class = VODoingBusinessAsSerializer
        payload = fakedata.VODoingBusinessAsTestDataCreate()
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
        

    def test_voDoingBusinessAsIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voDoingBusinessAs/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VODoingBusinessAsTestDataCreate()
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
        

    def test_voDoingBusinessAsIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voDoingBusinessAs/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VODoingBusinessAsTestDataCreate()
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
        payload = fakedata.VODoingBusinessAsTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_voLocationTypesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOLocationTypeTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/voLocationTypes/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_voLocationTypesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voLocationTypes"
        # Create:
        serializer_class = VOLocationTypeSerializer
        payload = fakedata.VOLocationTypeTestDataCreate()
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
        

    def test_voLocationTypesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voLocationTypes/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOLocationTypeTestDataCreate()
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
        

    def test_voLocationTypesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voLocationTypes/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOLocationTypeTestDataCreate()
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
        payload = fakedata.VOLocationTypeTestDataUpdate()
        jsonString = json.dumps(payload)
        response = self.client.put(updateUrl, content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_200_OK == response.status_code
        # Cleanup:
        deleteUrl = createUrl + "/" + str(createdId) + "/delete"
        response = self.client.post(deleteUrl)
        # Check that the response is OK.
        assert status.HTTP_204_NO_CONTENT == response.status_code
        

    def test_voOrgTypesBulkPost(self):
        # Test Bulk Load.
        payload = fakedata.VOTypeTestDataCreate()
        jsonString = "[]"
        response = self.client.post('/api/v1/voOrgTypes/bulk',content_type='application/json', data=jsonString)
        # Check that the response is 200 OK.
        assert status.HTTP_201_CREATED == response.status_code
        

    def test_voOrgTypesGet(self):
        # Test Create and List operations.
        testUrl = "/api/v1/voOrgTypes"
        # Create:
        serializer_class = VOTypeSerializer
        payload = fakedata.VOTypeTestDataCreate()
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
        

    def test_voOrgTypesIdDeletePost(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voOrgTypes/(?P<id>[0-9]+)/delete"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)/delete","")
        # Create an object:
        payload = fakedata.VOTypeTestDataCreate()
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
        

    def test_voOrgTypesIdGet(self):
        # Test Retrieve and Update operations.
        testUrl = "/api/v1/voOrgTypes/(?P<id>[0-9]+)"
        createUrl = testUrl.replace ("/(?P<id>[0-9]+)","")
        # Create an object:
        payload = fakedata.VOTypeTestDataCreate()
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
        payload = fakedata.VOTypeTestDataUpdate()
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




