import logging

import coreapi

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    schema,
)
from rest_framework import permissions
from rest_framework.schemas import AutoSchema

from rest_framework.response import Response
from django.http import JsonResponse
from django.http import Http404

from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.Topic import Topic

from api.indy import eventloop
from api.indy.agent import Verifier

from api_v2.indy.issuer import IssuerManager, IssuerException
from api_v2.indy.credential_offer import CredentialOfferManager
from api_v2.indy.credential import Credential, CredentialManager
from api_v2.indy.proof_request import ProofRequest
from api_v2.indy.proof import ProofManager

from api_v2.decorators.jsonschema import validate
from api_v2.jsonschema.issuer import ISSUER_JSON_SCHEMA
from api_v2.jsonschema.credential_offer import CREDENTIAL_OFFER_JSON_SCHEMA
from api_v2.jsonschema.credential import CREDENTIAL_JSON_SCHEMA
from api_v2.jsonschema.construct_proof import CONSTRUCT_PROOF_JSON_SCHEMA

logger = logging.getLogger(__name__)


@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
# @permission_classes((IsSignedRequest,))
@validate(CREDENTIAL_OFFER_JSON_SCHEMA)
def generate_credential_request(request, *args, **kwargs):
    """
    Processes a credential definition and responds with a credential request
    which can then be used to submit a credential.

    Example request payload:

    ```json
    {
        'credential_offer': <credential offer json>,
        'credential_definition': <credential definition json>
    }
    ```

    returns:

    ```
    {
        "credential_request": <credential request json>,
        "credential_request_metadata": <credential request metadata json>
    }
    ```
    """

    logger.warn(">>> Generate credential request")

    credential_offer = request.data["credential_offer"]
    credential_definition = request.data["credential_definition"]
    credential_offer_manager = CredentialOfferManager(
        credential_offer, credential_definition
    )

    credential_request, credential_request_metadata = (
        credential_offer_manager.generate_credential_request()
    )

    result = {
        "credential_request": credential_request,
        "credential_request_metadata": credential_request_metadata,
    }

    logger.warn("<<< Generate credential request")
    return JsonResponse({"success": True, "result": result})


@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
# @permission_classes((IsSignedRequest,))
@validate(CREDENTIAL_JSON_SCHEMA)
def store_credential(request, *args, **kwargs):
    """  
    Stores a verifiable credential in wallet.

    The data in the credential is parsed and stored in the database
    for search/display purposes based on the issuer's processor config.
    The data is then made available through a REST API as well as a 
    search API.

    Example request payload:

    ```json
    {
        "credential_data": <credential data>,
        "credential_request_metadata": <credential request metadata>
    }
    ```

    returns: created verified credential model
    """
    logger.warn(">>> Store Credential")

    credential_data = request.data["credential_data"]
    credential_request_metadata = request.data["credential_request_metadata"]

    logger.info(credential_data)

    credential = Credential(credential_data)
    credential_manager = CredentialManager(
        credential, credential_request_metadata
    )

    credential_wallet_id = credential_manager.process()

    return Response({"success": True, "result": credential_wallet_id})


@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@validate(ISSUER_JSON_SCHEMA)
# TODO: Clean up abstraction. IssuerManager writes only –
#       use serializer in view to return created models?
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
        "credential_types": [
            {
                "schema": "schema name",
                "version": "schema version",
                "description": "schema display name (english)",
                "endpoint": "url for issuing claims",
                "topic": {
                    "parent_source_id_claim": "parent_source_id",
                    "parent_source_name_claim": "parent_source_name",
                    "source_id_claim": "parent_source_id",
                    "parent_source_id_claim": "parent_source_id"
                },
                "mapping": [
                    {
                        "model": "name",
                        "fields": {
                            "text": {
                                "input": "legal_name",
                                "from": "claim"
                            },
                            "type": {
                                "input": "legal_name",
                                "from": "value"
                            }
                        }
                    },
                    {
                        "model": "address",
                        "fields": {
                            "addressee": {
                                "input": "addressee",
                                "from": "claim"
                            },
                            "civic_address": {
                                "input": "address_line_1",
                                "from": "claim"
                            },
                            "city": {
                                "input": "city",
                                "from": "claim"
                            },
                            "province": {
                                "input": "province",
                                "from": "claim"
                            },
                            "postal_code": {
                                "input": "postal_code",
                                "from": "claim"
                            },
                            "country": {
                                "input": "country",
                                "from": "claim"
                            },
                            "address_type": {
                                "input": "operating",
                                "from": "value"
                            }
                        }
                    },
                    {
                        "model": "address",
                        "fields": {
                            "addressee": {
                                "input": "addressee",
                                "from": "claim"
                            },
                            "civic_address": {
                                "input": "address_line_1",
                                "from": "claim",
                                "processor": [
                                    "string_helpers.uppercase",
                                    "string_helper.lowercase"
                                ]
                            },
                            "city": {
                                "input": "city",
                                "from": "claim"
                            },
                            "province": {
                                "input": "province",
                                "from": "claim"
                            },
                            "postal_code": {
                                "input": "postal_code",
                                "from": "claim"
                            },
                            "country": {
                                "input": "country",
                                "from": "claim"
                            },
                            "address_type": {
                                "input": "operating",
                                "from": "value"
                            }
                        }
                    }
                ]
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
                    "origin_did": "6qnvgJtqwK44D8LFYnV5Yf"
                },
                {
                    "id": 2,
                    "name": "doing_business_as.bc_registries",
                    "version": "1.0.31",
                    "origin_did": "6qnvgJtqwK44D8LFYnV5Yf"
                }
            ],
            "credential_types": [
                {
                    "id": 1,
                    "schema_id": 1,
                    "issuer_id": 1,
                    "description": "Incorporation",
                    "processor_config": null
                },
                {
                    "id": 2,
                    "schema_id": 2,
                    "issuer_id": 1,
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
        response = {"success": True, "result": updated}
    except IssuerException as e:
        logger.exception("Issuer request not accepted:")
        response = {"success": False, "result": str(e)}
    logger.warn("<<< Register issuer")
    return JsonResponse(response)


@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@validate(CONSTRUCT_PROOF_JSON_SCHEMA)
def construct_proof(request, *args, **kwargs):
    """  
    Constructs a proof given a proof request and source_id

    ```json
    {
        "proof_request": <HL Indy proof request>,
        "source_id": <source if of subject>
    }
    ```

    returns: HL Indy proof data
    """
    logger.warn(">>> Construct Proof")
    source_id = request.data["source_id"]
    proof_request = request.data["proof_request"]

    proof_manager = ProofManager(proof_request, source_id)
    proof = proof_manager.construct_proof()

    return JsonResponse({"success": True, "result": proof})


@api_view(["Get"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
@schema(
    AutoSchema(
        manual_fields=[
            coreapi.Field(
                "topic_type",
                required=True,
                location="query",
                description="The topic type to retrieve for this credential. e.g., 'incorporation'",
            )
        ]
    )
)
def verify_credential(request, *args, **kwargs):
    """  
    Constructs a proof request for a credential stored in the
    application database, constructs a proof for that proof 
    request, and then verifies it.

    returns: 

    ```json
    {
        "verified": <verification successful boolean>,
        "proof": <proof json>,
        "proof_request": <proof_request json>,
    }
    ```
    """
    logger.warn(">>> Verify Credential")
    credential_id = kwargs.get("id")
    topic_type = request.query_params.get("topic_type")
    if not credential_id:
        raise Http404

    if not topic_type:
        return JsonResponse(
            {
                "success": False,
                "result": "Request must include topic_type query parameter",
            }
        )

    try:
        credential = CredentialModel.objects.get(id=credential_id)
    except CredentialModel.DoesNotExist as error:
        logger.warn(error)
        raise Http404

    proof_request = ProofRequest(name="the-org-book", version="1.0.0")
    proof_request.build_from_credential(credential)

    topic = Topic.objects.get(credentials=credential, type=topic_type)

    proof_manager = ProofManager(proof_request.dict, topic.source_id)
    proof = proof_manager.construct_proof()

    async def verify():
        async with Verifier() as verifier:
            return await verifier.verify_proof(proof_request.dict, proof)

    verified = eventloop.do(verify())

    return JsonResponse(
        {
            "success": verified,
            "result": {
                "verified": verified,
                "proof": proof,
                "proof_request": proof_request.dict,
            },
        }
    )
