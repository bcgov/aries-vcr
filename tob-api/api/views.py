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

import asyncio
from api.claimDefProcesser import ClaimDefProcesser
from api.proofRequestProcesser import ProofRequestProcesser
from api.indy.claimDefParser import ClaimDefParser
from api.claimProcesser import ClaimProcesser
import json
import os
import random
import logging

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions 
from rest_framework import mixins
from rest_framework import generics
from rest_framework_bulk import BulkCreateModelMixin
from . import serializers
from auditable.views import AuditableMixin
from .models.DoingBusinessAs import DoingBusinessAs
from .models.InactiveClaimReason import InactiveClaimReason
from .models.IssuerService import IssuerService
from .models.Jurisdiction import Jurisdiction
from .models.Location import Location
from .models.LocationType import LocationType
from .models.VerifiableClaim import VerifiableClaim
from .models.VerifiableClaimType import VerifiableClaimType
from .models.VerifiableOrg import VerifiableOrg
from .models.VerifiableOrgType import VerifiableOrgType


class doingbusinessasBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of DoingBusinessAs object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = DoingBusinessAs.objects.all()  
  serializer_class = serializers.DoingBusinessAsSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new DoingBusinessAs objects
    """
    return self.create(request, *args, **kwargs)

class doingbusinessasGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available DoingBusinessAs objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = DoingBusinessAs.objects.all()  
  serializer_class = serializers.DoingBusinessAsSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available DoingBusinessAs objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new DoingBusinessAs object
    """
    return self.create(request, *args, **kwargs)

class doingbusinessasIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific DoingBusinessAs object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = DoingBusinessAs.objects.all()  
  serializer_class = serializers.DoingBusinessAsSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified DoingBusinessAs object
    """
    return self.destroy(request, *args, **kwargs)


class doingbusinessasIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific DoingBusinessAs object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = DoingBusinessAs.objects.all()  
  serializer_class = serializers.DoingBusinessAsSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified DoingBusinessAs object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified DoingBusinessAs object
    """
    return self.update(request, *args, **kwargs)

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

class locationsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of Location object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Location.objects.all()  
  serializer_class = serializers.LocationSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new Location objects
    """
    return self.create(request, *args, **kwargs)

class locationsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available Location objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Location.objects.all()  
  serializer_class = serializers.LocationSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available Location objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new Location object
    """
    return self.create(request, *args, **kwargs)

class locationsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific Location object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Location.objects.all()  
  serializer_class = serializers.LocationSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified Location object
    """
    return self.destroy(request, *args, **kwargs)


class locationsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific Location object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = Location.objects.all()  
  serializer_class = serializers.LocationSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified Location object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified Location object
    """
    return self.update(request, *args, **kwargs)

class locationtypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of LocationType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = LocationType.objects.all()  
  serializer_class = serializers.LocationTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new LocationType objects
    """
    return self.create(request, *args, **kwargs)

class locationtypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available LocationType objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = LocationType.objects.all()  
  serializer_class = serializers.LocationTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available LocationType objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new LocationType object
    """
    return self.create(request, *args, **kwargs)

class locationtypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific LocationType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = LocationType.objects.all()  
  serializer_class = serializers.LocationTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified LocationType object
    """
    return self.destroy(request, *args, **kwargs)


class locationtypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific LocationType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = LocationType.objects.all()  
  serializer_class = serializers.LocationTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified LocationType object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified LocationType object
    """
    return self.update(request, *args, **kwargs)

class verifiableclaimsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VerifiableClaim object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaim.objects.all()  
  serializer_class = serializers.VerifiableClaimSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VerifiableClaim objects
    """
    return self.create(request, *args, **kwargs)

class verifiableclaimsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VerifiableClaim objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaim.objects.all()  
  serializer_class = serializers.VerifiableClaimSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VerifiableClaim objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VerifiableClaim object
    """
    return self.create(request, *args, **kwargs)

class verifiableclaimsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VerifiableClaim object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaim.objects.all()  
  serializer_class = serializers.VerifiableClaimSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VerifiableClaim object
    """
    return self.destroy(request, *args, **kwargs)


class verifiableclaimsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VerifiableClaim object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaim.objects.all()  
  serializer_class = serializers.VerifiableClaimSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VerifiableClaim object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VerifiableClaim object
    """
    return self.update(request, *args, **kwargs)

class verifiableclaimtypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VerifiableClaimType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaimType.objects.all()  
  serializer_class = serializers.VerifiableClaimTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VerifiableClaimType objects
    """
    return self.create(request, *args, **kwargs)

class verifiableclaimtypesGet(AuditableMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VerifiableClaimType objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaimType.objects.all()  
  serializer_class = serializers.VerifiableClaimTypeSerializer
  
  def __init__(self) -> None:
    self.__logger = logging.getLogger(__name__)

  def get(self, request, *args, **kwargs):
    """
    Lists available VerifiableClaimType objects
    """
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    """
    Creates a new VerifiableClaimType object
    """
    data = request.data
    self.__logger.debug("\nPosting VerifiableClaimType(s):\n{0}\n".format(data))
    return self.create(request, *args, **kwargs)

class verifiableclaimtypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VerifiableClaimType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaimType.objects.all()  
  serializer_class = serializers.VerifiableClaimTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VerifiableClaimType object
    """
    return self.destroy(request, *args, **kwargs)


class verifiableclaimtypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VerifiableClaimType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableClaimType.objects.all()  
  serializer_class = serializers.VerifiableClaimTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VerifiableClaimType object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VerifiableClaimType object
    """
    return self.update(request, *args, **kwargs)

class verifiableorgsBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VerifiableOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrg.objects.all()  
  serializer_class = serializers.VerifiableOrgSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VerifiableOrg objects
    """
    return self.create(request, *args, **kwargs)

class verifiableorgsGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VerifiableOrg objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrg.objects.all()  
  serializer_class = serializers.VerifiableOrgSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VerifiableOrg objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VerifiableOrg object
    """
    return self.create(request, *args, **kwargs)

class verifiableorgsIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VerifiableOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrg.objects.all()  
  serializer_class = serializers.VerifiableOrgSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VerifiableOrg object
    """
    return self.destroy(request, *args, **kwargs)


class verifiableorgsIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VerifiableOrg object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrg.objects.all()
  serializer_class = serializers.VerifiableOrgDetailSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VerifiableOrg object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VerifiableOrg object
    """
    return self.update(request, *args, **kwargs)

class verifiableorgtypesBulkPost(AuditableMixin,BulkCreateModelMixin, generics.GenericAPIView):
  """  
  Bulk create / update a number of VerifiableOrgType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrgType.objects.all()  
  serializer_class = serializers.VerifiableOrgTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Creates a number of new VerifiableOrgType objects
    """
    return self.create(request, *args, **kwargs)

class verifiableorgtypesGet(AuditableMixin,mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  """  
  Lists available VerifiableOrgType objects  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrgType.objects.all()  
  serializer_class = serializers.VerifiableOrgTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Lists available VerifiableOrgType objects
    """
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    """
    Creates a new VerifiableOrgType object
    """
    return self.create(request, *args, **kwargs)

class verifiableorgtypesIdDeletePost(AuditableMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
  """  
  Deletes a specific VerifiableOrgType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrgType.objects.all()  
  serializer_class = serializers.VerifiableOrgTypeSerializer
  def post(self, request, *args, **kwargs):
    """
    Destroys the specified VerifiableOrgType object
    """
    return self.destroy(request, *args, **kwargs)


class verifiableorgtypesIdGet(AuditableMixin,mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
  """  
  Gets a specific VerifiableOrgType object  
  """
  lookup_field = 'id'
  permission_classes = (permissions.AllowAny,)  
  queryset = VerifiableOrgType.objects.all()  
  serializer_class = serializers.VerifiableOrgTypeSerializer
  def get(self, request, *args, **kwargs):
    """
    Retrieves the specified VerifiableOrgType object
    """
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    """
    Updates the specified VerifiableOrgType object
    """
    return self.update(request, *args, **kwargs)