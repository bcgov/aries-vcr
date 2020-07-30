import json
import logging
import time
import os
import random

import requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.v2.models.Credential import Credential as CredentialModel
from api.v2.utils import log_timing_method, log_timing_event
from agent_webhooks.utils.credential import Credential, CredentialManager
from agent_webhooks.utils.issuer import IssuerManager

LOGGER = logging.getLogger(__name__)

TOPIC_CONNECTIONS = "connections"
TOPIC_CONNECTIONS_ACTIVITY = "connections_activity"
TOPIC_CREDENTIALS = "issue_credential"
TOPIC_PRESENTATIONS = "presentations"
TOPIC_PRESENT_PROOF = "present_proof"
TOPIC_GET_ACTIVE_MENU = "get-active-menu"
TOPIC_PERFORM_MENU_ACTION = "perform-menu-action"
TOPIC_ISSUER_REGISTRATION = "issuer_registration"

PROCESS_INBOUND_CREDENTIALS = os.environ.get('PROCESS_INBOUND_CREDENTIALS', 'true')
if PROCESS_INBOUND_CREDENTIALS.upper() == "TRUE":
    LOGGER.debug(">>> YES processing inbound credentials")
    PROCESS_INBOUND_CREDENTIALS = True
else:
    LOGGER.error(">>> NO not processing inbound credentials")
    PROCESS_INBOUND_CREDENTIALS = False

RANDOM_ERRORS = os.environ.get('RANDOM_ERRORS', 'false').upper() == "TRUE"
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
    if topic == TOPIC_CONNECTIONS:
        response = Response("")

    elif topic == TOPIC_CONNECTIONS_ACTIVITY:
        response = Response("")

    elif topic == TOPIC_CREDENTIALS:
        response = handle_credentials(state, message)

    elif topic == TOPIC_PRESENTATIONS or topic == TOPIC_PRESENT_PROOF:
        response = handle_presentations(state, message)

    elif topic == TOPIC_GET_ACTIVE_MENU:
        response = Response("")

    elif topic == TOPIC_PERFORM_MENU_ACTION:
        response = Response("")

    elif topic == TOPIC_ISSUER_REGISTRATION:
        response = handle_register_issuer(message)

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
                if 1 == random.randint(1,50):
                    print("Raise exception 1 for " + credential_exchange_id)
                    raise Exception("Depliberate error to test problem reporting 1")
                if 1 == random.randint(1,50):
                    print("Return processing error 1 for " + credential_exchange_id)
                    return Response("Deliberate error to test bad request 1", status=status.HTTP_400_BAD_REQUEST)

            credential_data = {
                "thread_id": message["thread_id"],
                "schema_id": raw_credential["schema_id"],
                "cred_def_id": raw_credential["cred_def_id"],
                "rev_reg_id": raw_credential["rev_reg_id"],
                "attrs": {},
            }

            for attr in raw_credential["values"]:
                credential_data["attrs"][attr] = raw_credential["values"][attr]["raw"]

            existing = False
            if PROCESS_INBOUND_CREDENTIALS:
                credential = Credential(credential_data)

                # sanity check that we haven't received this credential yet
                credential_id = credential.thread_id
                existing_credential = CredentialModel.objects.filter(credential_id=credential_id)
                if 0 < len(existing_credential):
                    # TODO - credential already exists in the database, what to do?
                    LOGGER.error(" >>> Received duplicate for credential_id: " + credential_id + ", exch id: " + credential_exchange_id)
                    existing = True
                    ret_credential_id = credential_id
                else:
                    # new credential, populate database
                    credential = credential_manager.process(credential)
                    ret_credential_id = credential.credential_id
            else:
                ret_credential_id = credential_data["thread_id"]

            # check if the credential is in the wallet already
            if existing:
                resp = requests.get(
                    f"{settings.AGENT_ADMIN_URL}/credential"
                    + f"/{ret_credential_id}",
                    headers=settings.ADMIN_REQUEST_HEADERS,
                )
                if resp.status_code == 404:
                    existing = False

            # Instruct the agent to store the credential in wallet
            if not existing:
                resp = requests.post(
                    f"{settings.AGENT_ADMIN_URL}/issue-credential/records"
                    + f"/{credential_exchange_id}/store",
                    json={"credential_id": ret_credential_id},
                    headers=settings.ADMIN_REQUEST_HEADERS,
                )
                if resp.status_code == 404:
                    # TODO assume the credential exchange has completed?
                    resp = requests.get(
                        f"{settings.AGENT_ADMIN_URL}/credential"
                        + f"/{ret_credential_id}",
                        headers=settings.ADMIN_REQUEST_HEADERS,
                    )
                    if resp.status_code == 404:
                        LOGGER.error(" >>> Error cred exchange id is missing but credential is not available for " + credential_exchange_id + ", " + ret_credential_id)
                        return Response("Error cred exchange id is missing but credential is not available", status=status.HTTP_400_BAD_REQUEST)
                    pass
                else:
                    resp.raise_for_status()

            # You can include this exception to test error reporting
            if RANDOM_ERRORS:
                if 1 == random.randint(1,50):
                    print("Return error 2 for " + credential_exchange_id)
                    return Response("Deliberate error to test bad request 2", status=status.HTTP_400_BAD_REQUEST)
            
            response_data = {
                "success": True,
                "details": f"Received credential with id {ret_credential_id}",
            }

        # TODO other scenarios
        elif state == "stored":
            LOGGER.debug("Credential Stored")
            response_data = {"success": True, "details": "Credential Stored"}

    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(f"Send problem report for {credential_exchange_id}")
        # Send a problem report for the error
        resp = requests.post(
            f"{settings.AGENT_ADMIN_URL}/issue-credential/records/{credential_exchange_id}/problem-report",
            json={"explain_ltxt": str(e)},
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
            resp = requests.get(
                f"{settings.AGENT_ADMIN_URL}/credential/"
                + f"{cred_id}",
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
            wallet_credential = resp.json()
            wallet_credentials = {
                "cred_info": wallet_credential,
                "interval": None,
                "presentation_referents": requested_attribute_referents + requested_predicates_referents
            }
            credentials = [wallet_credentials,]
            credential_query = presentation_request["name"]

        if 0 == len(credentials):
            resp = requests.get(
                f"{settings.AGENT_ADMIN_URL}/present-proof/records/"
                + f"{message['presentation_exchange_id']}/credentials/"
                + f"{referents}",
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
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
            if (
                related_referent
                in credentials_for_presentation["requested_attributes"]
            ):
                credentials_for_presentation["requested_attributes"][
                    related_referent
                ]["cred_id"] = credential_id
                credentials_for_presentation["requested_attributes"][
                    related_referent
                ]["revealed"] = True
            elif (
                related_referent
                in credentials_for_presentation["requested_predicates"]
            ):
                credentials_for_presentation["requested_predicates"][
                    related_referent
                ]["cred_id"] = credential_id
                credentials_for_presentation["requested_predicates"][
                    related_referent
                ]["revealed"] = True
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
        resp = requests.post(
            f"{settings.AGENT_ADMIN_URL}/present-proof/records/"
            + f"{presentation_exchange_id}/send-presentation",
            json=credentials_for_presentation,
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
                        "category_labels": {"category": "label"},
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
                        "visible_fields": ["string"],
                        "logo_b64": "string",
                    }
                ],
                "issuer": {
                    "name": "string",
                    "did": "string",
                    "abbreviation": "string",
                    "email": "string",
                    "url": "string",
                    "endpoint": "string",
                    "logo_b64": "string"
                }
            }
        }
    """
    issuer_manager = IssuerManager()
    updated = issuer_manager.register_issuer(message)

    # update tagging policy
    tag_policy_updates = {}
    cred_types = updated.credential_types
    for ctype in cred_types:
        tag_attrs = ctype.get_tagged_attributes()
        if tag_attrs:
            tag_policy_updates[ctype.credential_def_id] = tag_attrs

    return Response(
        content_type="application/json", data={"result": updated.serialize()}
    )
