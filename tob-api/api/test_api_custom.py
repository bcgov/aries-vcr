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
django.setup()

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
from api.claimProcesser import ClaimProcesser

# Custom API test cases. 
# If an API operation does not contains generated code then it is tested in this 
# file.
#
class Test_Api_Custom(TestCase):
    
    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(Test_Api_Custom, cls).setUpClass()
        django.setup()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # needed to setup django
        django.setup()


    def test_usersCurrentGet(self):
        self.skipTest("Not implemented")        

    def test_rolesIdPermissionsGet(self):
        self.skipTest("Not implemented")        

    def test_rolesIdUsersGet(self):
        self.skipTest("Not implemented")        

    def test_usersIdPermissionsGet(self):
        self.skipTest("Not implemented")        

    def test_usersIdRolesGet(self):
        self.skipTest("Not implemented")        

    def test_usersSearchGet(self):
        self.skipTest("Not implemented")        

    def test_verifiedorgsIdVerifiableclaimsGet(self):
        self.skipTest("Not implemented")
       
    def test_RecieveClaim(self):
      claim = fakedata.FakeClaim()
      claimProcesser = ClaimProcesser()
      claimProcesser.SaveClaim(claim)
      print("testing")

if __name__ == '__main__':
    unittest.main()




