import logging
import json

from api.auth import IsSignedRequest
from api.indy.proofRequestBuilder import ProofRequestBuilder
from api_v2.indy.issuer import IssuerManager, IssuerException
from api.claimDefProcesser import ClaimDefProcesser
from rest_framework.response import Response
from api import serializers
from api.proofRequestProcesser import ProofRequestProcesser


from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from api_v2.decorators.jsonschema import validate
from api_v2.jsonschema.issuer import ISSUER_JSON_SCHEMA
from api_v2.jsonschema.credential_request import CREDENTIAL_REQUEST_JSON_SCHEMA

from rest_framework import permissions
from api.claimProcesser import ClaimProcesser
from django.http import JsonResponse
from rest_framework.views import APIView

from api.models.VerifiableClaim import VerifiableClaim

logger = logging.getLogger(__name__)


# class generate_claim_request(APIView):
#     """
#     Generate a credential request from a given credential definition.
#     """

#     # permission_classes = (IsSignedRequest,)
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         """
#         Processes a claim definition and responds with a claim request which
#         can then be used to submit a claim.

#         Example request payload:

#         ```json
#         {
#           'credential_offer': <credential offer json>,
#           'claim_def': <claim definition json>
#         }
#         ```

#         returns: indy sdk claim request json
#         """
#         __logger = logging.getLogger(__name__)
#         __logger.warn(">>> Generate a claim request")
#         claimDef = request.body.decode("utf-8")
#         __logger.warn(json.dumps(claimDef, indent=2))
#         # claimDefProcesser = ClaimDefProcesser(claimDef)
#         # (
#         #     credential_request,
#         #     credential_request_metadata,
#         # ) = claimDefProcesser.GenerateClaimRequest()
#         # __logger.warn("<<< Generated claim request")
#         # return JsonResponse(
#         #     {
#         #         "credential_request": credential_request,
#         #         "credential_request_metadata_json": credential_request_metadata,
#         #     }
#         # )


# # ToDo:
# # * Refactor the saving process to use serializers, etc.
# # ** Make it work with generics.GenericAPIView
# # ** Using APIView for the moment so a serializer_class does not need to be defined;
# #    as we manually processing things for the moment.
# class bcovrinStoreClaim(APIView):
#     """
#     Store a verifiable claim.
#     """

#     # permission_classes = (IsSignedRequest,)  # FIXME - change to IsRegisteredIssuer
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         """
#         Stores a verifiable claim into a central wallet.

#         The data in the claim is parsed and stored in the database
#         for search/display purposes; making it available through
#         the other APIs.

#         Example request payload:

#         ```json
#         {
#           "claim_type": <schema name>,
#           "claim_data": <claim json>
#         }
#         ```

#         returns: created verifiableClaim model
#         """
#         __logger = logging.getLogger(__name__)
#         __logger.warn(">>> Store a claim")
#         claim = request.body.decode("utf-8")
#         claimProcesser = ClaimProcesser()
#         verifiableOrg = claimProcesser.SaveClaim(claim)
#         serializer = serializers.VerifiableOrgSerializer(verifiableOrg)
#         __logger.warn("<<< Stored claim")
#         return Response(serializer.data)


# class bcovrinConstructProof(APIView):
#     """
#     Generates a proof based on a set of filters.
#     """
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         """
#         Generates a proof from a proof request and set of filters.

#         Example request payload:

#         ```json
#         {
#           "filters": {
#             "legal_entity_id": "c914cd7d-1f44-44b2-a0d3-c0bea12067fa"
#           },
#           "proof_request": {
#             "name": "proof_request_name",
#             "version": "1.0.0",
#             "nonce": "1986273812765872",
#             "requested_attrs": {
#               "attr_1": {
#                 "name": "attr_1",
#                 "restrictions": [
#                   {
#                     "schema_key": {
#                       "did": "issuer_did",
#                       "name": "schema_name",
#                       "version": "schema_version"
#                     }
#                   }
#                 ]
#               }
#             },
#             "requested_predicates": {}
#           }
#         }
#         ```

#         returns: indy sdk proof json
#         """
#         __logger = logging.getLogger(__name__)
#         proofRequestWithFilters = request.body.decode("utf-8")
#         proofRequestProcesser = ProofRequestProcesser(proofRequestWithFilters)
#         proofResponse = proofRequestProcesser.ConstructProof()
#         return JsonResponse(proofResponse)


# class bcovrinVerifyCredential(APIView):
#     """
#     Verifies a verifiable claim
#     """
#     permission_classes = (permissions.AllowAny,)

#     def get(self, request, *args, **kwargs):
#         """
#         Verifies a verifiable claim given a verifiable claim id
#         """
#         __logger = logging.getLogger(__name__)
#         verifiableClaimId = self.kwargs.get("id")
#         if verifiableClaimId is not None:
#             verifiableClaim = VerifiableClaim.objects.get(id=verifiableClaimId)

#             claimType = verifiableClaim.claimType

#             issuerService = claimType.issuerServiceId

#             proofRequestBuilder = ProofRequestBuilder(
#                 claimType.schemaName, claimType.schemaVersion
#             )

#             proofRequestBuilder.matchCredential(
#                 verifiableClaim.claimJSON,
#                 claimType.schemaName,
#                 claimType.schemaVersion,
#                 issuerService.DID,
#             )

#             legal_entity_id = None
#             try:
#                 legal_entity_id = json.loads(verifiableClaim.claimJSON)["values"][
#                     "legal_entity_id"
#                 ]["raw"]
#                 __logger.debug("Claim for legal_entity_id: %s" %
#                                legal_entity_id)
#             except Error as e:
#                 # no-op
#                 self.__logger.debug("Claim for NO legal_entity_id")

#             proofRequest = proofRequestBuilder.asDict()
#             proofRequestWithFilters = {
#                 "filters": {"legal_entity_id": legal_entity_id},
#                 "proof_request": proofRequest,
#             }

#             proofRequestProcesser = ProofRequestProcesser(
#                 json.dumps(proofRequestWithFilters)
#             )
#             proofResponse = proofRequestProcesser.ConstructProof()

#             return JsonResponse({"success": True, "proof": proofResponse})

#         return JsonResponse({"success": False})


@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
# @permission_classes((IsSignedRequest,))
@validate(CREDENTIAL_REQUEST_JSON_SCHEMA)
def generate_credential_request(request, *args, **kwargs):
    """
    Processes a credential definition and responds with a credential request
    which can then be used to submit a credential.

    Example request payload:

    ```json
    {
        'credential-offer': <credential offer json>,
        'credential-definition': <credential definition json>
    }
    ```

    returns: indy sdk credential request json
    """

    logger.warn(">>> Generate a credential request")
    logger.warn(json.dumps(request.data, indent=2))
    return JsonResponse({})


@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@validate(ISSUER_JSON_SCHEMA)
def register_issuer(request, *args, **kwargs):
    """  
    Processes an issuer definition and creates or updates the
    corresponding records. Responds with the updated issuer
    definition including record IDs.

    Example request payload:

    ```json
    {
        "issuer": {
            "did": "issuer DID",
            "name": "issuer name (english)",
            "abbreviation": "issuer TLA (english)",
            "email": "administrator email",
            "url": "url for issuer details"
        },
        "credential-types": [
            {
                "schema": "schema name",
                "version": "schema version",
                "name": "schema display name (english)",
                "mapping": {
                    "source-id-key": "org_registry_ID",
                    "models": [
                        {
                            "name": "Name",
                            "fields": {
                                "name": {
                                    "from": "claim",
                                    "input": "org_name"
                                },
                                "language-code": {
                                    "from": "value",
                                    "input": "en"
                                }
                            }
                        },
                        {
                            "name": "Person",
                            "fields": {
                                "full_name": {
                                    "from": "claim",
                                    "input": "org_name"
                                },
                                "name-type": {
                                    "from": "value",
                                    "input": "good"
                                },
                                "start-date": {
                                    "from": "claim",
                                    "input": "effective_date",
                                    "processor": [
                                        "parseDate"
                                    ]
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }
    ```

    returns:
    
    ```
    {
        "success": true,
        "result": {
            "issuer": {
                "id": 1,
                "did": "6qnvgJtqwK44D8LFYnV5Yf",
                "name": "BC Corporate Registry",
                "abbreviation": "BCReg",
                "email": "bcreg.test.issuer@example.ca",
                "url": "http://localhost:5000"
            },
            "schemas": [
                {
                    "id": 1,
                    "name": "incorporation.bc_registries",
                    "version": "1.0.31",
                    "publisher_did": "6qnvgJtqwK44D8LFYnV5Yf"
                },
                {
                    "id": 2,
                    "name": "doing_business_as.bc_registries",
                    "version": "1.0.31",
                    "publisher_did": "6qnvgJtqwK44D8LFYnV5Yf"
                }
            ],
            "credential-types": [
                {
                    "id": 1,
                    "schema-id": 1,
                    "issuer-id": 1,
                    "description": "Incorporation",
                    "processor_config": null
                },
                {
                    "id": 2,
                    "schema-id": 2,
                    "issuer-id": 1,
                    "description": "Doing Business As",
                    "processor_config": null
                }
            ]
        }
    }
    ```
    """

    logger.warn(">>> Register issuer")
    try:
        issuer_manager = IssuerManager()
        updated = issuer_manager.register_issuer(request, request.data)
        logger.info(
            "Issuer registration response: \n" + json.dumps(updated, indent=2)
        )
        response = {"success": True, "result": updated}
    except IssuerException as e:
        logger.exception("Issuer request not accepted:")
        response = {"success": False, "result": str(e)}
    logger.warn("<<< Register issuer")
    return JsonResponse(response)
