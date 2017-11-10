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
import os
import json
from django.test import TestCase
from django.test import Client
import django
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework.parsers import JSONParser
from rest_framework import status

from .search_serializers import OrganizationSearchSerializer
from .search_serializers import NameSearchSerializer

from .test_api_simple import Test_Api_Simple
from .test_api_complex import Test_Api_Complex

class Test_Api_Seacrh(TestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(Test_Api_Seacrh, cls).setUpClass()
        django.setup()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()
        self.populateDatabase()

    def populateDatabase(self):
        # Giant Hack ...
        # Basically;
        # For the complex tests to work the database needs to be populated with 
        # data.  Running the various bulk tests is a quick and DIRTY way to 
        # accomplish this.
        Test_Api_Simple.test_usersBulkPost(self)
        Test_Api_Simple.test_rolesBulkPost(self)
        Test_Api_Simple.test_permissionsBulkPost(self)
        Test_Api_Complex.test_userrolesBulkPost(self)
        Test_Api_Complex.test_rolepermissionsBulkPost(self)

        Test_Api_Simple.test_inactiveclaimreasonsBulkPost(self)
        Test_Api_Simple.test_jurisdictionsBulkPost(self)
        Test_Api_Simple.test_verifiableorgtypesBulkPost(self)
        Test_Api_Simple.test_locationtypesBulkPost(self)
        Test_Api_Complex.test_issuerservicesBulkPost(self)
        Test_Api_Complex.test_verifiableclaimtypesBulkPost(self)
        Test_Api_Complex.test_verifiableorgsBulkPost(self)
        Test_Api_Complex.test_verifiableclaimsBulkPost(self)
        Test_Api_Complex.test_doingbusinessasBulkPost(self)
        Test_Api_Complex.test_locationsBulkPost(self)

    def test_OrganizationSearch(self):
        # Makes an assumption of the test data
        testUrl = "/api/v1/search/organization?text=gas"
        serializer_class = OrganizationSearchSerializer
        response = self.client.get(testUrl)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        self.assertIsNotNone(data)       
        self.assertTrue(len(data) > 0)

    def test_NameSearch(self):
        # Makes an assumption of the test data
        testUrl = "/api/v1/search/name?name=gas"
        serializer_class = NameSearchSerializer
        response = self.client.get(testUrl)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        jsonString = response.content.decode("utf-8")
        data = json.loads(jsonString)
        self.assertIsNotNone(data)       
        self.assertTrue(len(data) > 0)

if __name__ == '__main__':
    unittest.main()