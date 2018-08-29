import asyncio
import logging

from aiohttp import web
import django.db
import jsonschema
from vonx.indy.messages import \
    ProofRequest as VonxProofRequest, \
    ConstructedProof as VonxConstructedProof
import vonx.web.views as vonx_views

from tob_anchor.boot import indy_client, indy_holder_id, indy_verifier_id

from api.models.User import User

from api_v2.models.Credential import Credential as CredentialModel

from api_v2.indy.issuer import IssuerManager, IssuerException
from api_v2.indy.credential import Credential, CredentialManager, CredentialException
from api_v2.indy.proof_request import ProofRequest
from api_v2.indy.proof import ProofManager

from api_v2.jsonschema.issuer import ISSUER_JSON_SCHEMA
from api_v2.jsonschema.credential_offer import CREDENTIAL_OFFER_JSON_SCHEMA
from api_v2.jsonschema.credential import CREDENTIAL_JSON_SCHEMA
from api_v2.jsonschema.construct_proof import CONSTRUCT_PROOF_JSON_SCHEMA

from vonx.indy.errors import IndyError
from vonx.web.headers import (
    KeyCache,
    KeyFinderBase,
    IndyKeyFinder,
    verify_signature,
)

LOGGER = logging.getLogger(__name__)


class DjangoKeyFinder(KeyFinderBase):
    """
    Handle key lookup
    """
    async def _lookup_key(self, key_id: str, key_type: str) -> bytes:
        if key_type == "ed25519":
            return await _run_django(self._db_lookup, key_id)

    def _db_lookup(self, key_id: str) -> bytes:
        try:
            user = User.objects.get(DID=key_id)
            if user.verkey:
                verkey = bytes(user.verkey)
                LOGGER.info(
                    "Found verkey for DID '%s' in users table: '%s'",
                    key_id, verkey)
                return verkey
        except User.DoesNotExist:
            pass


INDY_KEYFINDER = IndyKeyFinder(indy_client(), indy_verifier_id())
DJANGO_KEYFINDER = DjangoKeyFinder(INDY_KEYFINDER)
KEY_CACHE = KeyCache(DJANGO_KEYFINDER)


async def _check_signature(request, use_cache: bool = True):
    if request.get("didauth"):
        return True, request["didauth"]
    try:
        result = await verify_signature(
            request.headers, KEY_CACHE if use_cache else INDY_KEYFINDER,
            request.method, request.path_qs)
        request["didauth"] = result
        ok = True
    except IndyError:
        LOGGER.exception("Signature validation error:")
        result = web.json_response({"success": False, "result": "Signature required"}, status=400)
        request["didauth"] = None
        ok = False
    return ok, result

def _run_django(proc, *args) -> asyncio.Future:
    def runner(proc, *args):
        #django.setup()
        try:
            ret = proc(*args)
            return ret
        finally:
            django.db.connections.close_all()

    return asyncio.get_event_loop().run_in_executor(None, runner, proc, *args)

def _validate_schema(data, schema):
    try:
        jsonschema.validate(data, schema)
        ok = True
        result = None
    except jsonschema.ValidationError as e:
        LOGGER.exception("Error validating schema:")
        response = {
            "success": False,
            "result": "Schema validation error: {}".format(e),
        }
        ok = False
        result = web.json_response(response, status=400)
    return ok, result


#@validate(CREDENTIAL_OFFER_JSON_SCHEMA)
async def generate_credential_request(request):
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

    ok, result = await _check_signature(request)
    if not ok:
        return result

    LOGGER.warn(">>> Generate credential request")
    result = await vonx_views.generate_credential_request(request, indy_holder_id())
    LOGGER.warn("<<< Generate credential request")

    return result


#@validate(CREDENTIAL_JSON_SCHEMA)
async def store_credential(request):
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

    ok, result = await _check_signature(request)
    if not ok:
        return result

    LOGGER.warn(">>> Store credential")
    result = await vonx_views.store_credential(request, indy_holder_id())
    if result.get("stored"):
        def process(stored):
            credential = Credential(stored.cred.cred_data)
            credential_manager = CredentialManager(
                credential, stored.cred.cred_req_metadata
            )
            credential_manager.process(stored.cred_id)
        # run in a separate thread to avoid blocking the async loop
        try:
            await _run_django(process, result["stored"])
        except CredentialException as e:
            LOGGER.exception("Exception while processing credential")
            result = web.json_response({"success": False, "result": str(e)})
    LOGGER.warn("<<< Store credential")

    return result


# TODO: Clean up abstraction. IssuerManager writes only –
#       use serializer in view to return created models?
async def register_issuer(request):
    """
    Processes an issuer definition and creates or updates the
    corresponding records. Responds with the updated issuer
    definition including record IDs.

    Example request payload:

    ```json
    {
        "issuer": {
            "did": "6qnvgJtqwK44D8LFYnV5Yf", // required
            "name": "BC Corporate Registry", // required
            "abbreviation": "BCReg",
            "email": "bcreg.test.issuer@example.ca",
            "url": "http://localhost:5000"
        },
        "credential_types": [
            {
            "name": "Incorporation",
            "schema": "incorporation.bc_registries",
            "version": "1.0.31",
            "endpoint": "http://localhost:5000/bcreg/incorporation",
            "topic": {
                "source_id": {
                    "input": "corp_num",
                    "from": "claim"
                },
                "type": {
                    "input": "incorporation",
                    "from": "value"
                }
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
                }
            ]
            },
            {
            "name": "Doing Business As",
            "schema": "doing_business_as.bc_registries",
            "version": "1.0.31",
            "endpoint": "http://localhost:5000/bcreg/dba",
            "topic": {
                "parent_source_id": {
                    "input": "org_registry_id",
                    "from": "claim"
                },
                "parent_type": {
                    "input": "incorporation",
                    "from": "value"
                },
                "source_id": {
                    "input": "dba_corp_num",
                    "from": "claim"
                },
                "type": {
                    "input": "doing_business_as",
                    "from": "value"
                }
            },
            "mapping": [
                {
                "model": "name",
                "fields": {
                    "text": {
                        "input": "dba_name",
                        "from": "claim"
                    },
                    "type": {
                        "input": "dba_name",
                        "from": "value"
                    }
                }
                }
            ]
            },
            {
            "name": "Corporate Address",
            "schema": "address.bc_registries",
            "version": "1.0.31",
            "endpoint": "http://localhost:5000/bcreg/address",
            "topic": [
                {
                    "parent_source_id": {
                        "input": "org_registry_id",
                        "from": "claim"
                    },
                    "parent_type": {
                        "input": "incorporation",
                        "from": "value"
                    },
                    "source_id": {
                        "input": "dba_corp_num",
                        "from": "claim"
                    },
                    "type": {
                        "input": "doing_business_as",
                        "from": "value"
                    }
                },
                {
                    "source_id": {
                        "input": "org_registry_id",
                        "from": "claim"
                    },
                    "type": {
                        "input": "incorporation",
                        "from": "value"
                    }
                }
            ],
            "cardinality_fields": ["addr_type"],
            "mapping": [
                {
                    "model": "address",
                    "fields": {
                        "addressee": {
                            "input": "addressee",
                            "from": "claim"
                        },
                        "civic_address": {
                            "input": "local_address",
                            "from": "claim"
                        },
                        "city": {
                            "input": "municipality",
                            "from": "claim"
                        },
                        "province": {
                            "input": "province",
                            "from": "claim"
                        },
                        "postal_code": {
                            "input": "postal_code",
                            "from": "claim",
                            "processor": ["string_helpers.uppercase"]
                        },
                        "country": {
                            "input": "country",
                            "from": "claim"
                        },
                        "type": {
                            "input": "addr_type",
                            "from": "claim"
                        },
                        "end_date": {
                            "input": "end_date",
                            "from": "claim"
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

    # not using lookup on users table
    ok, didauth = await _check_signature(request, False)
    if not ok:
        return didauth

    data = await request.json()
    ok, result = _validate_schema(data, ISSUER_JSON_SCHEMA)
    if not ok:
        return result

    def process(request, data):
        try:
            issuer_manager = IssuerManager()
            updated = issuer_manager.register_issuer(didauth, data)
            KEY_CACHE._cache_invalidate(didauth["keyId"], didauth["algorithm"])
            return {"success": True, "result": updated}
        except IssuerException as e:
            LOGGER.exception("Issuer request not accepted:")
            return {"success": False, "result": str(e)}

    LOGGER.warn(">>> Register issuer")
    response = await _run_django(process, request, data)
    LOGGER.warn("<<< Register issuer")

    return web.json_response(response)


#@validate(CONSTRUCT_PROOF_JSON_SCHEMA)
async def construct_proof(request):
    """
    Constructs a proof given a proof request

    ```json
    {
        "proof_request": <HL Indy proof request>
    }
    ```

    returns: HL Indy proof data
    """

    ok, result = await _check_signature(request)
    if not ok:
        return result

    LOGGER.warn(">>> Construct proof")
    result = await vonx_views.construct_proof(request, indy_holder_id())
    LOGGER.warn("<<< Construct proof")

    return result


async def verify_credential(request):
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
    LOGGER.warn(">>> Verify credential")
    credential_id = request.match_info.get("id")

    if not credential_id:
        return web.json_response({"success": False, "result": "Credential ID not provided"}, status=400)

    def fetch_cred(credential_id):
        try:
            return CredentialModel.objects.get(id=credential_id)
        except CredentialModel.DoesNotExist:
            return None
    credential = await _run_django(fetch_cred, credential_id)
    if not credential:
        LOGGER.warn("Credential not found: %s", credential_id)
        return web.json_response({"success": False, "result": "Credential not found"}, status=404)

    proof_request = ProofRequest(name="the-org-book", version="1.0.0")
    proof_request.build_from_credential(credential)

    proof_manager = ProofManager(proof_request.dict, {credential.wallet_id})
    proof = await proof_manager.construct_proof_async()

    verified = await indy_client().verify_proof(
            indy_verifier_id(),
            VonxProofRequest(proof_request.dict),
            VonxConstructedProof(proof))
    verified = verified.verified == "true"
    LOGGER.warn("<<< Verify credential")

    return web.json_response(
        {
            "success": verified,
            "result": {
                "verified": verified,
                "proof": proof,
                "proof_request": proof_request.dict,
            },
        }
    )


async def status(request, *args, **kwargs):
    result = await indy_client().get_status()
    return web.json_response(result)
