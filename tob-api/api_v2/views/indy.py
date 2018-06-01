import logging
import json

from api.auth import IsSignedRequest
from api.indy.proofRequestBuilder import ProofRequestBuilder

from api.claimDefProcesser import ClaimDefProcesser
from rest_framework.response import Response
from api import serializers
from api.proofRequestProcesser import ProofRequestProcesser

from api_v2.indy.issuer import IssuerManager, IssuerException
from api_v2.indy.credential_offer import CredentialOfferManager

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from api_v2.decorators.jsonschema import validate
from api_v2.jsonschema.issuer import ISSUER_JSON_SCHEMA
from api_v2.jsonschema.credential_offer import CREDENTIAL_OFFER_JSON_SCHEMA

from rest_framework import permissions
from api.claimProcesser import ClaimProcesser
from django.http import JsonResponse
from rest_framework.views import APIView

from api.models.VerifiableClaim import VerifiableClaim

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

    response = {
        "credential_request": credential_request,
        "credential_request_metadata": credential_request_metadata,
    }

    logger.warn("<<< Generate credential request")
    return JsonResponse(response)


@api_view(["POST"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
# @permission_classes((IsSignedRequest,))
@validate(CREDENTIAL_OFFER_JSON_SCHEMA)
def store_credential(request, *args, **kwargs):
    pass


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
        "credential_types": [
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
        logger.info(
            "Issuer registration response: \n" + json.dumps(updated, indent=2)
        )
        response = {"success": True, "result": updated}
    except IssuerException as e:
        logger.exception("Issuer request not accepted:")
        response = {"success": False, "result": str(e)}
    logger.warn("<<< Register issuer")
    return JsonResponse(response)
