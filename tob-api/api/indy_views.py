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
from rest_framework.response import Response
from api import serializers
from api.proofRequestProcesser import ProofRequestProcesser
import json
from rest_framework import permissions
from api.claimProcesser import ClaimProcesser
from django.http import JsonResponse
from rest_framework.views import APIView
from api.models.VerifiableClaim import VerifiableClaim

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
    Processes a claim definition and responds with a claim request which
    can then be used to submit a claim.

    Example request payload:

    ```json
    {
      'did': <issuer did>,
      'seqNo': <schema sequence number>,
      'claim_def': <claim definition json>
    }
    ```

    returns: indy sdk claim request json
    """
    claimDef = request.body.decode('utf-8')
    claimDefProcesser = ClaimDefProcesser(claimDef)
    claimRequest = claimDefProcesser.GenerateClaimRequest()
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

    Example request payload:

    ```json
    {
      "claim_type": <schema name>,
      "claim_data": <claim json>
    }
    ```

    returns: created verifiableClaim model
    """
    claim = request.body.decode('utf-8')
    claimProcesser = ClaimProcesser()
    verifiableOrg = claimProcesser.SaveClaim(claim)
    serializer = serializers.VerifiableOrgSerializer(verifiableOrg)
    return Response(serializer.data)

class bcovrinConstructProof(APIView):
  """  
  Generates a proof based on a set of filters.
  """
  permission_classes = (permissions.AllowAny,)  
 
  def post(self, request, *args, **kwargs):
    """  
    Generates a proof from a proof request and set of filters.

    Example request payload:

    ```json
    {
      "filters": {
        "legal_entity_id": "c914cd7d-1f44-44b2-a0d3-c0bea12067fa"
      },
      "proof_request": {
        "name": "proof_request_name",
        "version": "1.0.0",
        "nonce": "1986273812765872",
        "requested_attrs": {
          "attr_1": {
            "name": "attr_1",
            "restrictions": [
              {
                "schema_key": {
                  "did": "issuer_did",
                  "name": "schema_name",
                  "version": "schema_version"
                }
              }
            ]
          }
        },
        "requested_predicates": {}
      }
    }
    ```

    returns: indy sdk proof json
    """
    proofRequestWithFilters = request.body.decode('utf-8')
    proofRequestProcesser = ProofRequestProcesser(proofRequestWithFilters)
    proofResponse = proofRequestProcesser.ConstructProof()
    return JsonResponse(proofResponse)

class bcovrinVerifyCredential(APIView):
  """  
  Verifies a verifiable claim
  """
  permission_classes = (permissions.AllowAny,)  

  def post(self, request, *args, **kwargs):
    """
    Verifies a verifiable claim given a verifiable claim id
    """

    verifiableClaimId = self.kwargs.get('id')
    if verifiableClaimId is not None:
      verifiableClaim = VerifiableClaim.objects.get(id=verifiableClaimId)
      claimType = verifiableClaim.claimType

      print(claimType.schemaName)
      print(claimType.schemaVersion)

      return JsonResponse({'success': True})

    return JsonResponse({'success': False})
