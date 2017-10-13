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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions 
from rest_framework import mixins
from rest_framework import generics
from rest_framework_bulk import BulkCreateModelMixin
from . import serializers
from .models.CurrentUserViewModel import CurrentUserViewModel
from .models.InactiveClaimReason import InactiveClaimReason
from .models.IssuerService import IssuerService
from .models.Jurisdiction import Jurisdiction
from .models.Permission import Permission
from .models.PermissionViewModel import PermissionViewModel
from .models.Role import Role
from .models.RolePermission import RolePermission
from .models.RolePermissionViewModel import RolePermissionViewModel
from .models.RoleViewModel import RoleViewModel
from .models.User import User
from .models.UserDetailsViewModel import UserDetailsViewModel
from .models.UserRole import UserRole
from .models.UserRoleViewModel import UserRoleViewModel
from .models.UserViewModel import UserViewModel
from .models.VOClaim import VOClaim
from .models.VOClaimType import VOClaimType
from .models.VODoingBusinessAs import VODoingBusinessAs
from .models.VOLocation import VOLocation
from .models.VOLocationType import VOLocationType
from .models.VOType import VOType
from .models.VerifiedOrg import VerifiedOrg


# Custom views.  This file is hand edited.

class usersCurrentGet(APIView):
  """  
  Get the currently logged in user  
  """
  # enter code for this routine here.        
  
  def get(self, request, ):
    return Response()

class rolesIdPermissionsGet(APIView):
  """  
  Get all the permissions for a role  
  """
  # enter code for this routine here.        
  
  def get(self, request, id):
    return Response()

class rolesIdUsersGet(APIView):
  """  
  Gets all the users for a role  
  """
  # enter code for this routine here.        
  
  def get(self, request, id):
    return Response()

class usersIdPermissionsGet(APIView):
  """  
  Returns the set of permissions for a user  
  """
  # enter code for this routine here.        
  
  def get(self, request, id):
    return Response()

class usersIdRolesGet(APIView):
  """  
  Returns the roles for a user  
  """
  # enter code for this routine here.        
  
  def get(self, request, id):
    return Response()

class usersSearchGet(APIView):
  """  
  Searches Users  
  """
  # enter code for this routine here.        
  
  def get(self, request, fuelSuppliers = None, surname = None, includeInactive = None):
    return Response()

class verifiedorgsIdVoclaimsGet(APIView):
  """  
  Returns the VO Claims for a Verified Organization  
  """
  # enter code for this routine here.        
  
  def get(self, request, id):
    return Response()


