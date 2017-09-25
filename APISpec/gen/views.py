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
from .models.InactiveClaimReason import InactiveClaimReason
from .models.IssuerOrg import IssuerOrg
from .models.Jurisdiction import Jurisdiction
from .models.VOClaim import VOClaim
from .models.VOClaimType import VOClaimType
from .models.VODoingBusinessAs import VODoingBusinessAs
from .models.VOLocation import VOLocation
from .models.VOLocationType import VOLocationType
from .models.VOType import VOType
from .models.VerifiedOrg import VerifiedOrg


class inactiveClaimReasonsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class inactiveClaimReasonsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class inactiveClaimReasonsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class inactiveClaimReasonsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

class issuerOrgsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of IssuerOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerOrg.objects.all()  
  serializer_class = serializers.IssuerOrgSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new IssuerOrg objects
    """
    return self.create(request, *args, **kwargs)

class issuerOrgsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available IssuerOrg objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerOrg.objects.all()  
  serializer_class = serializers.IssuerOrgSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available IssuerOrg objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new IssuerOrg object
    """
    return self.create(request, *args, **kwargs)

class issuerOrgsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific IssuerOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerOrg.objects.all()  
  serializer_class = serializers.IssuerOrgSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified IssuerOrg object
    """
    return self.destroy(request, *args, **kwargs)


class issuerOrgsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific IssuerOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = IssuerOrg.objects.all()  
  serializer_class = serializers.IssuerOrgSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified IssuerOrg object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified IssuerOrg object
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

class voClaimsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class voClaimsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class voClaimsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class voClaimsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

class voClaimTypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class voClaimTypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class voClaimTypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class voClaimTypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

class voDoingBusinessAsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class voDoingBusinessAsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class voDoingBusinessAsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class voDoingBusinessAsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

class voLocationsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class voLocationsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class voLocationsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class voLocationsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

class voLocationTypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class voLocationTypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class voLocationTypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class voLocationTypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

class voOrgTypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class voOrgTypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class voOrgTypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class voOrgTypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

class verifiedOrgsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
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

class verifiedOrgsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

class verifiedOrgsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
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


class verifiedOrgsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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

