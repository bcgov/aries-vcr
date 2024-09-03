import base64
import json
import logging
import os
import random
import time

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from marshmallow import ValidationError
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.v2.models.Credential import Credential as CredentialModel
from api.v2.utils import log_timing_method, log_timing_event, call_agent_with_retry

from agent_webhooks.handlers.vc_di_issuer import handle_issuer as handle_vc_di_issuer
from agent_webhooks.handlers.vc_di_credential_type import (
    handle_credential_type as handle_vc_di_credential_type,
)
from agent_webhooks.handlers.vc_di_credential import (
    handle_credential as handle_vc_di_credential,
)
from agent_webhooks.utils.credential import Credential, CredentialManager
from agent_webhooks.utils.issuer import IssuerManager

LOGGER = logging.getLogger(__name__)

TOPIC_CONNECTIONS = "connections"
TOPIC_CONNECTIONS_ACTIVITY = "connections_activity"
TOPIC_CREDENTIALS = "issue_credential"
TOPIC_CREDENTIALS_2_0 = "issue_credential_v2_0"
TOPIC_CREDENTIALS_2_0_INDY = "issue_credential_v2_0_indy"
TOPIC_PRESENTATIONS = "presentations"
TOPIC_PRESENT_PROOF = "present_proof"
TOPIC_ISSUER_REGISTRATION = "issuer_registration"
TOPIC_VC_DI_ISSUER = "vc_di_issuer"
TOPIC_VC_DI_CREDENTIAL_TYPE = "vc_di_credential_type"
TOPIC_VC_DI_CREDENTIAL = "vc_di_credential"

PROCESS_INBOUND_CREDENTIALS = os.environ.get("PROCESS_INBOUND_CREDENTIALS", "true")
if PROCESS_INBOUND_CREDENTIALS.upper() == "TRUE":
    LOGGER.debug(">>> YES processing inbound credentials")
    PROCESS_INBOUND_CREDENTIALS = True
else:
    LOGGER.error(">>> NO not processing inbound credentials")
    PROCESS_INBOUND_CREDENTIALS = False

RANDOM_ERRORS = os.environ.get("RANDOM_ERRORS", "false").upper() == "TRUE"
if RANDOM_ERRORS:
    LOGGER.error(">>> YES generating random credential processing errors")


@swagger_auto_schema(method="post", auto_schema=None)
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def agent_callback(request, topic):
    message = request.data

    if "state" not in message:
        LOGGER.warn(f"Received aca-py webhook without state. message={message}")

    state = message["state"] if "state" in message else None
    LOGGER.debug(f"Received aca-py webhook. state={state} message={message}")

    start_time = time.perf_counter()
    method = "agent_callback." + topic + ("." + state if state else "")
    log_timing_event(method, message, start_time, None, False)

    # dispatch based on the topic type
    if topic == TOPIC_CONNECTIONS or topic == TOPIC_CONNECTIONS_ACTIVITY:
        response = Response("")

    elif topic == TOPIC_CREDENTIALS:
        response = handle_credentials(state, message)

    elif topic == TOPIC_CREDENTIALS_2_0 or topic == TOPIC_CREDENTIALS_2_0_INDY:
        response = handle_credentials_2_0(state, message)

    elif topic == TOPIC_PRESENTATIONS or topic == TOPIC_PRESENT_PROOF:
        response = handle_presentations(state, message)

    elif topic == TOPIC_ISSUER_REGISTRATION:
        response = handle_register_issuer(message)

    elif topic == TOPIC_VC_DI_ISSUER:
        try:
            result = handle_vc_di_issuer(message)
            response = Response(result.serialize())
        except ValidationError as err:
            response = Response(str(err), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as err:
            response = Response(str(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif topic == TOPIC_VC_DI_CREDENTIAL_TYPE:
        try:
            result = handle_vc_di_credential_type(message)
            response = Response(result.serialize())
        except ValidationError as err:
            response = Response(str(err), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as err:
            response = Response(str(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif topic == TOPIC_VC_DI_CREDENTIAL:
        try:
            result = handle_vc_di_credential(message)
            response = Response(result)
        except ValidationError as err:
            response = Response(str(err), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as err:
            response = Response(str(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        LOGGER.info("Callback: topic=" + topic + ", message=" + json.dumps(message))
        end_time = time.perf_counter()
        log_timing_method(method, start_time, end_time, False)
        log_timing_event(method, message, start_time, end_time, False)
        return Response("Invalid topic: " + topic, status=status.HTTP_400_BAD_REQUEST)

    end_time = time.perf_counter()
    log_timing_method(method, start_time, end_time, True)
    log_timing_event(method, message, start_time, end_time, True)

    return response


# create one global manager instance
credential_manager = CredentialManager()


def handle_credentials(state, message):
    """
    Receives notification of a credential processing event.

    For example, for a greenlight registration credential:
        message = {
            "connection_id": "12345",
            "credential_definition_id": "6qnvgJtqwK44D8LFYnV5Yf:3:CL:25:tag",
            "credential_exchange_id": "666",
            "credential_id": "67890",
            "credential_offer": {},
            "credential_request": {},
            "credential_request_metadata": {},
            "credential": {
                "referent": "67892",
                "values":
                    {
                        "address_line_1": "2230 Holdom Avenue",
                        "address_line_2": "",
                        "addressee": "Ms. Brenda J Strachan",
                        "city": "Surrey",
                        "corp_num": "FM0243624",
                        "country": "CA",
                        "entity_name_effective": "2007-08-30",
                        "entity_status": "Active",
                        "entity_status_effective": "2007-08-30",
                        "entity_type": "BC Company",
                        "legal_name": "LOEFFLER PIZZA PLACE LIMITED",
                        "postal_code": "V3T 4Y5",
                        "province": "BC",
                        "reason_description": "Filing:REGST",
                        "registration_date": "2007-08-30"
                    },
                "schema_id": "6qnvgJtqwK44D8LFYnV5Yf:2:Registered Corporation:1.0.3",
                "cred_def_id": "6qnvgJtqwK44D8LFYnV5Yf:3:CL:25:tag",
                "rev_reg_id": null,
                "rev_reg": null,
                "witness": "Ian",
                "cred_rev_id": null,
                "signature": "ian costanzo, honest",
                "signature_correctness_proof": "honest"
            },
            "initiator": "...",
            "schema_id": "...",
            "state": "stored",
            "thread_id": "..."
        }
    """

    credential_exchange_id = message["credential_exchange_id"]
    LOGGER.debug(
        f'Credential: state="{state}" credential_exchange_id="{credential_exchange_id}"'
    )
    response_data = {}

    try:
        if state == "offer_received":
            LOGGER.debug("After receiving credential offer, send credential request")
            # no need to perform a task, we run the agent with the --auto-respond-credential-offer flag set
            response_data = {
                "success": True,
                "details": f"Received offer on credential exchange {credential_exchange_id}",
            }

        elif state == "credential_received":
            raw_credential = message["raw_credential"]

            # You can include this exception to test error reporting
            if RANDOM_ERRORS:
                raise_random_exception(credential_exchange_id, "credential_recieved")

            credential_data = {
                "thread_id": message["thread_id"],
                "schema_id": raw_credential["schema_id"],
                "cred_def_id": raw_credential["cred_def_id"],
                "rev_reg_id": (
                    raw_credential["rev_reg_id"]
                    if "rev_reg_id" in raw_credential
                    else None
                ),
                "attrs": {},
            }

            for attr in raw_credential["values"]:
                credential_data["attrs"][attr] = raw_credential["values"][attr]["raw"]

            return receive_credential(credential_exchange_id, credential_data)

        elif state == "stored":
            LOGGER.debug("Credential Stored")
            response_data = {"success": True, "details": "Credential Stored"}

    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(f"Send problem report for {credential_exchange_id}")
        # Send a problem report for the error
        resp = call_agent_with_retry(
            f"{settings.AGENT_ADMIN_URL}/issue-credential/records/{credential_exchange_id}/problem-report",
            post_method=True,
            payload={"description": str(e)},
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        resp.raise_for_status()
        return Response({"success": False, "error": str(e)})

    return Response(response_data)


def handle_presentations(state, message):
    LOGGER.debug(f" >>>> handle_presentations({state})")

    if state == "request_received":
        presentation_request = message["presentation_request"]
        presentation_exchange_id = message["presentation_exchange_id"]

        # Pull referents out of presentation request
        requested_attribute_referents = list(
            presentation_request["requested_attributes"].keys()
        )
        requested_predicates_referents = list(
            presentation_request["requested_predicates"].keys()
        )

        # Comma delimit all referents for agent API request
        referents = ",".join(
            requested_attribute_referents + requested_predicates_referents
        )
        credentials = []

        if presentation_request["name"].startswith("cred_id::"):
            cred_id = presentation_request["name"][9:]
            resp = call_agent_with_retry(
                f"{settings.AGENT_ADMIN_URL}/credential/" + f"{cred_id}",
                post_method=False,
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
            resp.raise_for_status()
            wallet_credential = resp.json()
            wallet_credentials = {
                "cred_info": wallet_credential,
                "interval": None,
                "presentation_referents": requested_attribute_referents
                + requested_predicates_referents,
            }
            credentials = [
                wallet_credentials,
            ]
            credential_query = presentation_request["name"]

        if 0 == len(credentials):
            resp = call_agent_with_retry(
                f"{settings.AGENT_ADMIN_URL}/present-proof/records/"
                + f"{message['presentation_exchange_id']}/credentials/"
                + f"{referents}",
                post_method=False,
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
            resp.raise_for_status()
            # All credentials from wallet that satisfy presentation request
            credentials = resp.json()
            credential_query = f"/present-proof/records/{message['presentation_exchange_id']}/credentials/{referents}"

        # Prep the payload we need to send to the agent API
        credentials_for_presentation = {
            "self_attested_attributes": {},
            "requested_attributes": {},
            "requested_predicates": {},
        }
        for referent in requested_attribute_referents:
            credentials_for_presentation["requested_attributes"][referent] = {}

        for referent in requested_predicates_referents:
            credentials_for_presentation["requested_predicates"][referent] = {}

        # we should have a single credential at this point
        results_length = len(credentials)
        if results_length != 1:
            raise Exception(
                "Number of credentials returned by query "
                + f"{credential_query} was not 1, it was {results_length}"
            )

        credential = credentials[0]

        credential_id = credential["cred_info"]["referent"]

        # For all "presentation_referents" on this `credential` returned
        # from the wallet, we can apply this credential_id as the selected
        # credential for the presentation
        for related_referent in credential["presentation_referents"]:
            if related_referent in credentials_for_presentation["requested_attributes"]:
                credentials_for_presentation["requested_attributes"][related_referent][
                    "cred_id"
                ] = credential_id
                credentials_for_presentation["requested_attributes"][related_referent][
                    "revealed"
                ] = True
            elif (
                related_referent in credentials_for_presentation["requested_predicates"]
            ):
                credentials_for_presentation["requested_predicates"][related_referent][
                    "cred_id"
                ] = credential_id
                credentials_for_presentation["requested_predicates"][related_referent][
                    "revealed"
                ] = True
            else:
                raise Exception(
                    f"Referent {related_referent} returned from wallet "
                    + "was not expected in proof request."
                )

        # We should have a fully constructed presentation now.
        # Let's check to make sure:
        for referent in credentials_for_presentation["requested_attributes"]:
            if credentials_for_presentation["requested_attributes"][referent] == {}:
                raise Exception(
                    f"requested_attributes contains unfulfilled referent {referent}"
                )

        for referent in credentials_for_presentation["requested_predicates"]:
            if credentials_for_presentation["requested_predicates"][referent] == {}:
                raise Exception(
                    f"requested_predicates contains unfulfilled referent {referent}"
                )

        # Finally, we should be able to send this payload to the agent for it
        # to finish the process and send the presentation back to the verifier
        # (to be verified)
        resp = call_agent_with_retry(
            f"{settings.AGENT_ADMIN_URL}/present-proof/records/"
            + f"{presentation_exchange_id}/send-presentation",
            post_method=True,
            payload=credentials_for_presentation,
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        resp.raise_for_status()

    return Response()


def handle_register_issuer(message):
    """Handles the registration of a new issuing agent in the credential registry.

    The agent registration credential will be in the following format:
    {
         "issuer_registration_id": "string",
         "connection_id": "string",
         "issuer_registration": {
             "credential_types": [
                 {
                     "claim_descriptions": {"claim": "description"},
                     "claim_labels": {"claim": "label"},
                     "credential_def_id": "string",
                     "schema": "string",
                     "version": "string",
                     "name": "string",
                     "credential": {
                         "effective_date": {"input": "topic_id", "from": "claim"}
                     },
                     "topic": [
                         {
                             "source_id": {"input": "topic_id", "from": "claim"}
                         }
                     ],
                     "endpoint": "string",
                     "cardinality_fields": ["string"],
                     "mapping": {},
                 }
             ],
             "issuer": {
                 "name": "string",
                 "did": "string",
                 "abbreviation": "string",
                 "email": "string",
                 "url": "string",
                 "endpoint": "string",
             }
         }
     }
    """
    issuer_manager = IssuerManager()
    updated = issuer_manager.register_issuer(message)

    # reset the global CredentialManager instance (to clear the CredentialType cache)
    global credential_manager
    credential_manager = CredentialManager()

    return Response(
        content_type="application/json", data={"result": updated.serialize()}
    )


def handle_credentials_2_0(state, message):
    """
    Receives notification of a credential 2.0 processing event.

    For example, for a registration credential:

    message = {
        "cred_proposal": { ... },
        "role": "issuer",
        "initiator": "self",
        "created_at": "2021-04-30 02:54:32.925351Z",
        "conn_id": "ae5f0b97-746e-4062-bdf2-27b9d6809cc9",
        "auto_issue": true,
        "cred_preview": { ... },
        "cred_ex_id": "e2f41814-d625-4218-9f53-879111398372",
        "cred_request": { ... },
        "auto_offer": false,
        "state": "credential-issued",
        "updated_at": "2021-04-30 02:54:33.138119Z",
        "cred_issue": {
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/issue-credential",
            "@id": "0f0104e6-43ca-47e1-85e0-4fd41b10688f",
            "formats": [
                {
                    "attach_id": "0",
                    "format": "hlindy-zkp-v1.0"
                }
            ],
            "credentials~attach": [
                {
                    "@id": "0",
                    "mime-type": "application/json",
                    "data": {
                        "base64": "..."
                    }
                }
            ]
        },
        "cred_offer": { ... },
        "thread_id": "dd56313f-1787-47f7-8838-d6931284ae30"
    }
    """

    cred_ex_id = message["cred_ex_id"]
    LOGGER.debug(f'Credential: state="{state}" cred_ex_id="{cred_ex_id}"')
    response_data = {}

    try:
        if state == "offer-received":
            LOGGER.debug("After receiving credential offer, send credential request")
            # no need to perform a task, we run the agent with the --auto-respond-credential-offer flag set
            response_data = {
                "success": True,
                "details": f"Received offer on credential exchange {cred_ex_id}",
            }

        elif state == "credential-received":
            cred_issue = message["cred_issue"]
            if cred_issue is None:
                LOGGER.error(" >>> Error cred_issue missing for " + cred_ex_id)
                return Response(
                    "Error cred_issue missing for credential",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # You can include this exception to test error reporting
            if RANDOM_ERRORS:
                raise_random_exception(cred_ex_id, "credential-recieved")

            cred_data = {}
            for cred_fmt in cred_issue["formats"]:
                att_id = cred_fmt["attach_id"]
                cred_att = [
                    att
                    for att in cred_issue["credentials~attach"]
                    if att["@id"] == att_id
                ][0]
                if cred_att is None:
                    LOGGER.error(
                        " >>> Error data cred_att could not be parsed for " + cred_ex_id
                    )
                    return Response(
                        "Error credential attachment could not be parsed from cred_issue",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cred_raw_base64 = cred_att["data"]["base64"]
                cred_raw = json.loads(base64.b64decode(cred_raw_base64))

                if cred_raw is None:
                    LOGGER.error(
                        " >>> Error data cred_issue could not be parsed for "
                        + cred_ex_id
                    )
                    return Response(
                        "Error credential data could not be parsed from cred_issue",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cred_data = {
                    "thread_id": cred_issue["~thread"]["thid"],
                    "schema_id": cred_raw["schema_id"],
                    "cred_def_id": cred_raw["cred_def_id"],
                    "rev_reg_id": (
                        cred_raw["rev_reg_id"] if "rev_reg_id" in cred_raw else None
                    ),
                    "attrs": {k: v["raw"] for k, v in cred_raw["values"].items()},
                }

            return receive_credential(cred_ex_id, cred_data, "2.0")

        else:
            LOGGER.warn(f"Handler for state: {state} not implemented")
            response_data = {"success": True, "details": f"State received {state}"}

    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(f"Send problem report for {cred_ex_id}")
        # Send a problem report for the error
        resp = call_agent_with_retry(
            f"{settings.AGENT_ADMIN_URL}/issue-credential-2.0/records/{cred_ex_id}/problem-report",
            post_method=True,
            payload={"description": str(e)},
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        resp.raise_for_status()
        return Response({"success": False, "error": str(e)})

    return Response(response_data)


def receive_credential(cred_ex_id, cred_data, v=None):
    try:
        existing = False
        if PROCESS_INBOUND_CREDENTIALS:
            credential = Credential(cred_data)

            # sanity check that we haven't received this credential yet
            cred_id = credential.thread_id
            existing_credential = CredentialModel.objects.filter(credential_id=cred_id)
            if 0 < len(existing_credential):
                # TODO - credential already exists in the database, what to do?
                LOGGER.error(
                    " >>> Received duplicate for credential_id: "
                    + cred_id
                    + ", exch id: "
                    + cred_ex_id
                )
                existing = True
                ret_cred_id = cred_id
            else:
                # new credential, populate database
                credential = credential_manager.process(credential)
                ret_cred_id = credential.credential_id
        else:
            ret_cred_id = cred_data["thread_id"]

        # check if the credential is in the wallet already
        if existing:
            resp = call_agent_with_retry(
                f"{settings.AGENT_ADMIN_URL}/credential/{ret_cred_id}",
                post_method=False,
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
            if resp.status_code == 404:
                existing = False

        # Instruct the agent to store the credential in wallet
        if not existing:
            # post with retry - if returned status is 503 unavailable retry a few times
            resp = call_agent_with_retry(
                f"{settings.AGENT_ADMIN_URL}/issue-credential{'-' + v if v else ''}/records/{cred_ex_id}/store",
                post_method=True,
                payload={"credential_id": ret_cred_id},
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
            if resp.status_code == 404:
                # TODO assume the credential exchange has completed?
                resp = call_agent_with_retry(
                    f"{settings.AGENT_ADMIN_URL}/credential/{ret_cred_id}",
                    post_method=False,
                    headers=settings.ADMIN_REQUEST_HEADERS,
                )
                if resp.status_code == 404:
                    LOGGER.error(
                        " >>> Error cred exchange id is missing but credential is not available for "
                        + cred_ex_id
                        + ", "
                        + ret_cred_id
                    )
                    return Response(
                        "Error cred exchange id is missing but credential is not available",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                pass
            else:
                resp.raise_for_status()

        response_data = {
            "success": True,
            "details": f"Received credential with id {ret_cred_id}",
        }

        return Response(response_data)
    except Exception as e:
        raise e


def raise_random_exception(cred_ex_id, method=""):
    if 1 == random.randint(1, 50):
        print(f"Raise random exception for {cred_ex_id} from method: {method}")
        raise Exception("Deliberate error to test problem reporting")
