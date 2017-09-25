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


# Custom API test cases. 
# If an API operation does not contains generated code then it is tested in this 
# file.
#
class Test_Api_Custom(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()


if __name__ == '__main__':
    unittest.main()




