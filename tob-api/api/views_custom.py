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
  def get(self, request, ):
    currentUser = User.objects.all()[0] # replace with current user
    serializer = serializers.UserSerializer(currentUser)
    return Response(serializer.data)

class rolesIdPermissionsGet(APIView):
  def get(self, request, id):
    """  
    Get all the permissions for a role  
    """
    role = Role.objects.get(id=id)
    rolePermissions = RolePermission.objects.filter(roleId=role)
    serializer = serializers.RolePermissionSerializer(rolePermissions, many=True)
    return Response(serializer.data)

class rolesIdUsersGet(APIView):
  def get(self, request, id):
    """  
    Gets all the users for a role  
    """
    role = Role.objects.get(id=id)
    userRoles = UserRole.objects.filter(roleId=role)
    serializer = serializers.UserRoleSerializer(userRoles, many=True)
    return Response(serializer.data)

class usersIdPermissionsGet(APIView):
  def get(self, request, id):
    """
    Returns the set of permissions for a user
    """
    user = User.objects.get(id=id)
    userRoles = UserRole.objects.filter(userId=user)
    result = []
    for userRole in userRoles:
        rolePermissions = RolePermission.objects.filter(roleId=userRole.roleId)
        for rolePermission in rolePermissions:
            result.append (rolePermission.permissionId)
    serializer = serializers.PermissionSerializer(result, many=True)
    return Response(serializer.data)

class usersIdRolesGet(APIView):
  def get(self, request, id):
    """
    Returns all roles that a user is a member of
    """
    result = UserRole.objects.filter(userId=id)
    serializer = serializers.UserRoleSerializer(result, many=True)
    return Response(serializer.data)

class usersSearchGet(APIView):
  def get(self, request, fuelSuppliers = None, surname = None, includeInactive = None):
    """
    Searches Users
    """
    result = User.objects.all()
    if surname != None:
       result = result.filter(surname__icontains = surname)

    serializer = serializers.UserSerializer(result, many=True)
    return Response(serializer.data)

class verifiedorgsIdVoclaimsGet(APIView):
  def get(self, request, id):
    """  
    Returns the Claims for a Verified Organization  
    """
    org = VerifiedOrg.objects.get(id=id)
    claims = VOClaim.objects.filter(verifiedOrgId=org)
    serializer = serializers.VOClaimSerializer(claims, many=True)
    return Response(serializer.data)

class verifiedorgsIdVoDoingBusinessAsGet(APIView):
  def get(self, request, id):
    """  
    Returns the Doing Business As information for a Verified Organization  
    """
    org = VerifiedOrg.objects.get(id=id)
    dbas = VODoingBusinessAs.objects.filter(verifiedOrgId=org)
    serializer = serializers.VODoingBusinessAsSerializer(dbas, many=True)
    return Response(serializer.data)

class verifiedorgsIdVoLocationsGet(APIView):
  def get(self, request, id):
    """  
    Returns the locations for a Verified Organization  
    """
    org = VerifiedOrg.objects.get(id=id)
    locations = VOLocation.objects.filter(verifiedOrgId=org)
    serializer = serializers.VOLocationSerializer(locations, many=True)
    return Response(serializer.data)