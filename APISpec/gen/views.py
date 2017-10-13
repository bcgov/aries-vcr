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
from auditable.views import AuditableMixin
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


class inactiveclaimreasonsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of InactiveClaimReason object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = InactiveClaimReason.objects.all()  
  serializer_class = serializers.InactiveClaimReasonSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new InactiveClaimReason objects
    """
    return self.create(request, *args, **kwargs)

class inactiveclaimreasonsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available InactiveClaimReason objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = InactiveClaimReason.objects.all()  
  serializer_class = serializers.InactiveClaimReasonSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available InactiveClaimReason objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new InactiveClaimReason object
    """
    return self.create(request, *args, **kwargs)

class inactiveclaimreasonsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific InactiveClaimReason object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = InactiveClaimReason.objects.all()  
  serializer_class = serializers.InactiveClaimReasonSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified InactiveClaimReason object
    """
    return self.destroy(request, *args, **kwargs)


class inactiveclaimreasonsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific InactiveClaimReason object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = InactiveClaimReason.objects.all()  
  serializer_class = serializers.InactiveClaimReasonSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified InactiveClaimReason object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified InactiveClaimReason object
    """
    return self.update(request, *args, **kwargs)

class issuerservicesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of IssuerService object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerService.objects.all()  
  serializer_class = serializers.IssuerServiceSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new IssuerService objects
    """
    return self.create(request, *args, **kwargs)

class issuerservicesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available IssuerService objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerService.objects.all()  
  serializer_class = serializers.IssuerServiceSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available IssuerService objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new IssuerService object
    """
    return self.create(request, *args, **kwargs)

class issuerservicesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific IssuerService object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerService.objects.all()  
  serializer_class = serializers.IssuerServiceSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified IssuerService object
    """
    return self.destroy(request, *args, **kwargs)


class issuerservicesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific IssuerService object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerService.objects.all()  
  serializer_class = serializers.IssuerServiceSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified IssuerService object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified IssuerService object
    """
    return self.update(request, *args, **kwargs)

class jurisdictionsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of Jurisdiction object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Jurisdiction.objects.all()  
  serializer_class = serializers.JurisdictionSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new Jurisdiction objects
    """
    return self.create(request, *args, **kwargs)

class jurisdictionsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available Jurisdiction objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Jurisdiction.objects.all()  
  serializer_class = serializers.JurisdictionSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available Jurisdiction objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new Jurisdiction object
    """
    return self.create(request, *args, **kwargs)

class jurisdictionsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific Jurisdiction object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Jurisdiction.objects.all()  
  serializer_class = serializers.JurisdictionSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified Jurisdiction object
    """
    return self.destroy(request, *args, **kwargs)


class jurisdictionsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific Jurisdiction object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Jurisdiction.objects.all()  
  serializer_class = serializers.JurisdictionSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified Jurisdiction object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified Jurisdiction object
    """
    return self.update(request, *args, **kwargs)

class permissionsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of Permission object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Permission.objects.all()  
  serializer_class = serializers.PermissionSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new Permission objects
    """
    return self.create(request, *args, **kwargs)

class permissionsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available Permission objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Permission.objects.all()  
  serializer_class = serializers.PermissionSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available Permission objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new Permission object
    """
    return self.create(request, *args, **kwargs)

class permissionsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific Permission object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Permission.objects.all()  
  serializer_class = serializers.PermissionSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified Permission object
    """
    return self.destroy(request, *args, **kwargs)


class permissionsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific Permission object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Permission.objects.all()  
  serializer_class = serializers.PermissionSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified Permission object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified Permission object
    """
    return self.update(request, *args, **kwargs)

class rolesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of Role object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Role.objects.all()  
  serializer_class = serializers.RoleSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new Role objects
    """
    return self.create(request, *args, **kwargs)

class rolesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available Role objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Role.objects.all()  
  serializer_class = serializers.RoleSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available Role objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new Role object
    """
    return self.create(request, *args, **kwargs)

class rolesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific Role object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Role.objects.all()  
  serializer_class = serializers.RoleSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified Role object
    """
    return self.destroy(request, *args, **kwargs)


class rolesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific Role object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Role.objects.all()  
  serializer_class = serializers.RoleSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified Role object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified Role object
    """
    return self.update(request, *args, **kwargs)

class rolepermissionsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of RolePermission object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = RolePermission.objects.all()  
  serializer_class = serializers.RolePermissionSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new RolePermission objects
    """
    return self.create(request, *args, **kwargs)

class rolepermissionsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available RolePermission objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = RolePermission.objects.all()  
  serializer_class = serializers.RolePermissionSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available RolePermission objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new RolePermission object
    """
    return self.create(request, *args, **kwargs)

class rolepermissionsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific RolePermission object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = RolePermission.objects.all()  
  serializer_class = serializers.RolePermissionSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified RolePermission object
    """
    return self.destroy(request, *args, **kwargs)


class rolepermissionsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific RolePermission object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = RolePermission.objects.all()  
  serializer_class = serializers.RolePermissionSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified RolePermission object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified RolePermission object
    """
    return self.update(request, *args, **kwargs)

class usersBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of User object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = User.objects.all()  
  serializer_class = serializers.UserSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new User objects
    """
    return self.create(request, *args, **kwargs)

class usersGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available User objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = User.objects.all()  
  serializer_class = serializers.UserSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available User objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new User object
    """
    return self.create(request, *args, **kwargs)

class usersIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific User object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = User.objects.all()  
  serializer_class = serializers.UserSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified User object
    """
    return self.destroy(request, *args, **kwargs)


class usersIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific User object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = User.objects.all()  
  serializer_class = serializers.UserSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified User object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified User object
    """
    return self.update(request, *args, **kwargs)

class userrolesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of UserRole object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = UserRole.objects.all()  
  serializer_class = serializers.UserRoleSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new UserRole objects
    """
    return self.create(request, *args, **kwargs)

class userrolesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available UserRole objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = UserRole.objects.all()  
  serializer_class = serializers.UserRoleSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available UserRole objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new UserRole object
    """
    return self.create(request, *args, **kwargs)

class userrolesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific UserRole object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = UserRole.objects.all()  
  serializer_class = serializers.UserRoleSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified UserRole object
    """
    return self.destroy(request, *args, **kwargs)


class userrolesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific UserRole object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = UserRole.objects.all()  
  serializer_class = serializers.UserRoleSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified UserRole object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified UserRole object
    """
    return self.update(request, *args, **kwargs)

class voclaimsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VOClaim object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaim.objects.all()  
  serializer_class = serializers.VOClaimSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VOClaim objects
    """
    return self.create(request, *args, **kwargs)

class voclaimsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VOClaim objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaim.objects.all()  
  serializer_class = serializers.VOClaimSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VOClaim objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VOClaim object
    """
    return self.create(request, *args, **kwargs)

class voclaimsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VOClaim object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaim.objects.all()  
  serializer_class = serializers.VOClaimSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VOClaim object
    """
    return self.destroy(request, *args, **kwargs)


class voclaimsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VOClaim object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaim.objects.all()  
  serializer_class = serializers.VOClaimSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VOClaim object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VOClaim object
    """
    return self.update(request, *args, **kwargs)

class voclaimtypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VOClaimType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaimType.objects.all()  
  serializer_class = serializers.VOClaimTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VOClaimType objects
    """
    return self.create(request, *args, **kwargs)

class voclaimtypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VOClaimType objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaimType.objects.all()  
  serializer_class = serializers.VOClaimTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VOClaimType objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VOClaimType object
    """
    return self.create(request, *args, **kwargs)

class voclaimtypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VOClaimType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaimType.objects.all()  
  serializer_class = serializers.VOClaimTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VOClaimType object
    """
    return self.destroy(request, *args, **kwargs)


class voclaimtypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VOClaimType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOClaimType.objects.all()  
  serializer_class = serializers.VOClaimTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VOClaimType object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VOClaimType object
    """
    return self.update(request, *args, **kwargs)

class vodoingbusinessasBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VODoingBusinessAs object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VODoingBusinessAs.objects.all()  
  serializer_class = serializers.VODoingBusinessAsSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VODoingBusinessAs objects
    """
    return self.create(request, *args, **kwargs)

class vodoingbusinessasGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VODoingBusinessAs objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VODoingBusinessAs.objects.all()  
  serializer_class = serializers.VODoingBusinessAsSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VODoingBusinessAs objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VODoingBusinessAs object
    """
    return self.create(request, *args, **kwargs)

class vodoingbusinessasIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VODoingBusinessAs object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VODoingBusinessAs.objects.all()  
  serializer_class = serializers.VODoingBusinessAsSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VODoingBusinessAs object
    """
    return self.destroy(request, *args, **kwargs)


class vodoingbusinessasIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VODoingBusinessAs object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VODoingBusinessAs.objects.all()  
  serializer_class = serializers.VODoingBusinessAsSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VODoingBusinessAs object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VODoingBusinessAs object
    """
    return self.update(request, *args, **kwargs)

class volocationsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VOLocation object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocation.objects.all()  
  serializer_class = serializers.VOLocationSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VOLocation objects
    """
    return self.create(request, *args, **kwargs)

class volocationsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VOLocation objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocation.objects.all()  
  serializer_class = serializers.VOLocationSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VOLocation objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VOLocation object
    """
    return self.create(request, *args, **kwargs)

class volocationsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VOLocation object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocation.objects.all()  
  serializer_class = serializers.VOLocationSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VOLocation object
    """
    return self.destroy(request, *args, **kwargs)


class volocationsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VOLocation object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocation.objects.all()  
  serializer_class = serializers.VOLocationSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VOLocation object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VOLocation object
    """
    return self.update(request, *args, **kwargs)

class volocationtypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VOLocationType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocationType.objects.all()  
  serializer_class = serializers.VOLocationTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VOLocationType objects
    """
    return self.create(request, *args, **kwargs)

class volocationtypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VOLocationType objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocationType.objects.all()  
  serializer_class = serializers.VOLocationTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VOLocationType objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VOLocationType object
    """
    return self.create(request, *args, **kwargs)

class volocationtypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VOLocationType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocationType.objects.all()  
  serializer_class = serializers.VOLocationTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VOLocationType object
    """
    return self.destroy(request, *args, **kwargs)


class volocationtypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VOLocationType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOLocationType.objects.all()  
  serializer_class = serializers.VOLocationTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VOLocationType object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VOLocationType object
    """
    return self.update(request, *args, **kwargs)

class voorgtypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VOType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOType.objects.all()  
  serializer_class = serializers.VOTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VOType objects
    """
    return self.create(request, *args, **kwargs)

class voorgtypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VOType objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOType.objects.all()  
  serializer_class = serializers.VOTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VOType objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VOType object
    """
    return self.create(request, *args, **kwargs)

class voorgtypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VOType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOType.objects.all()  
  serializer_class = serializers.VOTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VOType object
    """
    return self.destroy(request, *args, **kwargs)


class voorgtypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VOType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VOType.objects.all()  
  serializer_class = serializers.VOTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VOType object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VOType object
    """
    return self.update(request, *args, **kwargs)

class verifiedorgsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VerifiedOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiedOrg.objects.all()  
  serializer_class = serializers.VerifiedOrgSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VerifiedOrg objects
    """
    return self.create(request, *args, **kwargs)

class verifiedorgsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VerifiedOrg objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiedOrg.objects.all()  
  serializer_class = serializers.VerifiedOrgSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VerifiedOrg objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VerifiedOrg object
    """
    return self.create(request, *args, **kwargs)

class verifiedorgsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VerifiedOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiedOrg.objects.all()  
  serializer_class = serializers.VerifiedOrgSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VerifiedOrg object
    """
    return self.destroy(request, *args, **kwargs)


class verifiedorgsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VerifiedOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiedOrg.objects.all()  
  serializer_class = serializers.VerifiedOrgSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VerifiedOrg object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VerifiedOrg object
    """
    return self.update(request, *args, **kwargs)

