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

from api.claimDefProcesser import ClaimDefProcesser
from api.proofRequestProcesser import ProofRequestProcesser
import json
from rest_framework import permissions
from api.claimProcesser import ClaimProcesser
from django.http import JsonResponse
from rest_framework.views import APIView

# ToDo:
# * Refactor the saving process to use serializers, etc.
# ** Make it work with generics.GenericAPIView
# ** Using APIView for the moment so a serializer_class does not need to be defined; 
#    as we manually processing things for the moment.
class bcovrinGenerateClaimRequest(APIView):
  """  
  Generate a claim request from a given claim definition.
  """
  permission_classes = (permissions.AllowAny,)  
  
  def post(self, request, *args, **kwargs):
    """  
    Processes a claim definition and responds with a claim request which can then be used to submit a claim.
    """
    claimDef = request.body.decode('utf-8')
    claimDefProcesser = ClaimDefProcesser(claimDef)
    claimRequest = claimDefProcesser.GenerateClaimRequest()
    print("=-==-\n\n\n")
    print(claimRequest)
    return JsonResponse(json.loads(claimRequest))

# ToDo:
# * Refactor the saving process to use serializers, etc.
# ** Make it work with generics.GenericAPIView
# ** Using APIView for the moment so a serializer_class does not need to be defined; 
#    as we manually processing things for the moment.
class bcovrinStoreClaim(APIView):
  """  
  Store a verifiable claim.
  """
  permission_classes = (permissions.AllowAny,)  
 
  def post(self, request, *args, **kwargs):
    """  
    Stores a verifiable claim into a central wallet.

    The data in the claim is parsed and stored in the database
    for search/display purposes; making it available through
    the other APIs.
    """
    claim = request.body.decode('utf-8')
    claimProcesser = ClaimProcesser()
    claimProcesser.SaveClaim(claim)
    return JsonResponse({"success": True})


class bcovrinConstructProof(APIView):
  """  
  Generates a proof based on a set of filters.
  """
  permission_classes = (permissions.AllowAny,)  
 
  def post(self, request, *args, **kwargs):
    """  
    Generates a proof from a proof request and set of filters.
    """
    proofRequestWithFilters = request.body.decode('utf-8')
    proofRequestProcesser = ProofRequestProcesser(proofRequestWithFilters)
    proofResponse = proofRequestProcesser.ConstructProof()
    return JsonResponse(json.loads(proofResponse))
