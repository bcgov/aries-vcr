import logging

from urllib.parse import urlencode
import os

import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from icat_cbs.utils.credential import Credential, CredentialManager
from icat_cbs.utils.issuer import IssuerManager

AGENT_ADMIN_URL = os.environ.get("AGENT_ADMIN_URL")
AGENT_ADMIN_API_KEY = os.environ.get("AGENT_ADMIN_API_KEY")

ADMIN_REQUEST_HEADERS = {}
if AGENT_ADMIN_API_KEY is not None:
    ADMIN_REQUEST_HEADERS = {"x-api-key": AGENT_ADMIN_API_KEY}

LOGGER = logging.getLogger(__name__)

TOPIC_CONNECTIONS = "connections"
TOPIC_CREDENTIALS = "credentials"
TOPIC_PRESENTATIONS = "presentations"
TOPIC_GET_ACTIVE_MENU = "get-active-menu"
TOPIC_PERFORM_MENU_ACTION = "perform-menu-action"
TOPIC_ISSUER_REGISTRATION = "issuer_registration"


@swagger_auto_schema(method="post", auto_schema=None)
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def agent_callback(request, topic):
    message = request.data

    # dispatch based on the topic type
    if topic == TOPIC_CONNECTIONS:
        return handle_connections(message["state"], message)

    elif topic == TOPIC_CREDENTIALS:
        return handle_credentials(message["state"], message)

    elif topic == TOPIC_PRESENTATIONS:
        return handle_presentations(message["state"], message)

    elif topic == TOPIC_GET_ACTIVE_MENU:
        return handle_get_active_menu(message)

    elif topic == TOPIC_PERFORM_MENU_ACTION:
        return handle_perform_menu_action(message)

    elif topic == TOPIC_ISSUER_REGISTRATION:
        return handle_register_issuer(message)

    else:
        LOGGER.info("Callback: topic=", topic, ", message=", message)
        return Response("Invalid topic: " + topic, status=status.HTTP_400_BAD_REQUEST)


def handle_connections(state, message):
    # TODO auto-accept?
    print("handle_connections()", state)
    return Response(state)


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

    # global admin_url
    credential_exchange_id = message["credential_exchange_id"]
    print(
        "Credential: state=", state, ", credential_exchange_id=", credential_exchange_id
    )

    try:
        if state == "offer_received":
            print("After receiving credential offer, send credential request")
            # resp = requests.post(admin_url + '/credential_exchange/' + credential_exchange_id + '/send-request')
            # assert resp.status_code == 200
            return Response("")

        elif state == "credential_received":
            raw_credential = message["raw_credential"]

            print("Received credential:")
            # print(raw_credential)

            # TODO can include this exception to test error reporting
            # raise Exception("Depliberate error to test problem reporting")

            credential_data = {
                "schema_id": raw_credential["schema_id"],
                "cred_def_id": raw_credential["cred_def_id"],
                "rev_reg_id": raw_credential["rev_reg_id"],
                "attrs": {},
            }

            for attr in raw_credential["values"]:
                credential_data["attrs"][attr] = raw_credential["values"][attr]["raw"]

            credential = Credential(
                credential_data, credential_exchange_id=credential_exchange_id
            )

            credential_manager = CredentialManager()
            credential_manager.process(credential)

            # Instruct the agent to store the credential in wallet
            resp = requests.post(
                f"{AGENT_ADMIN_URL}/credential_exchange/{credential_exchange_id}/store",
                headers=ADMIN_REQUEST_HEADERS
            )
            resp.raise_for_status()
            assert resp.status_code == 200

            return Response({"success": True})

        # TODO other scenarios
        elif state == "stored":
            print("credential stored")
            # print(message)

    except Exception as e:
        LOGGER.error(str(e))
        # Send a problem report for the error
        resp = requests.post(
            f"{AGENT_ADMIN_URL}/credential_exchange/{credential_exchange_id}/problem_report",
            json={"explain_ltxt": str(e)},
            headers=ADMIN_REQUEST_HEADERS
        )
        resp.raise_for_status()
        assert resp.status_code == 200
        return Response({"success": False, "error": str(e)})

    return Response("")


def handle_presentations(state, message):
    print("handle_presentations()", state, message)
    presentation_request = message["presentation_request"]

    found_credentials = {"requested_attributes": {}, "requested_predicates": {}}
    """
    found_credentials looks like:
    {
        "requested_attributes": {
            "57281247-2a1e-4fde-9583-6e3f35b9c329": [
                {
                    "cred_info": {
                    "referent": "d4dbd617-15b2-4956-b898-559be7387566", // cred id
                    "attrs": {
                        "registration_date": "2019-01-01",
                        "province": "Random Text JFBEPF7A87OMXNNOND RCUFD3",
                        "address_line_1": "Random Text NQBG9FGHZS IB1RC3EE 6SGKL",
                        "registered_jurisdiction": "Random Text 52NVLRZMSPMEBGQHXQQ0",
                        "entity_status": "OPT1",
                        "city": "Random Text J572VD PN1M9H 74UJYSQVNXD",
                        "addressee": "Random Text S6RE6 YG7OO72L0LN4SIFPS51",
                        "entity_name": "Random Name 9BUKOAOGHJ",
                        "entity_status_effective": "2019-01-01",
                        "entity_name_effective": "2019-01-01",
                        "country": "Random Text GQ PVQ4BPS06JGAV1P39M0PC2",
                        "effective_date": "2019-01-01",
                        "entity_type": "Random Text ANU8VVI7ZOALW5XIXCOWCY4UV",
                        "corp_num": "b7c74cb8-93c6-4955-9d47-0389fa79b670",
                        "expiry_date": "2019-01-01",
                        "postal_code": "Random Text M9W4CZ H6XTUX2NQ54SFNL338"
                    },
                    "schema_id": "52Po5igEeRht8Qmhow:2:my-registration.nick-org:1.0.0",
                    "cred_def_id": "52Po5igEeRht8Qmhow:3:CL:10:default",
                    "rev_reg_id": null,
                    "cred_rev_id": null
                    },
                    "interval": null,
                    "presentation_referents": [
                        "57281247-2a1e-4fde-9583-6e3f35b9c329"
                    ]
                }
            ]
        },
        "requested_predicates": {}
    }
    """

    # Shim to add missing libindy functionality https://jira.hyperledger.org/browse/IS-1363
    for referent in presentation_request["requested_attributes"]:
        requested_attribute = presentation_request["requested_attributes"][referent]
        credentials_for_attr = []
        for restriction in requested_attribute["restrictions"]:
            query_params = {}
            query_params["extra_query"] = restriction
            query_params_enc = urlencode(query_params)
            resp = requests.get(
                f"{AGENT_ADMIN_URL}/presentation_exchange/"
                + f"{message['presentation_exchange_id']}/credentials/"
                + f"{referent}?{query_params_enc}"
            )

            credentials = resp.json()
            credentials_for_attr.extend(credentials)

        found_credentials["requested_attributes"][referent] = credentials_for_attr

    for referent in presentation_request["requested_predicates"]:
        requested_predicate = presentation_request["requested_predicates"][referent]
        credentials_for_pred = []
        for restriction in requested_predicate["restrictions"]:
            query_params = {}
            query_params["extra_query"] = restriction
            query_params_enc = urlencode(query_params)
            resp = requests.get(
                f"{AGENT_ADMIN_URL}/presentation_exchange/"
                + f"{message['presentation_exchange_id']}/credentials/"
                + f"{referent}?{query_params_enc}"
            )

            credentials = resp.json()
            credentials_for_pred.extend(credentials)

        found_credentials["requested_predicates"][referent] = credentials_for_pred
    # end shim

    # 


    credentials_for_pr = {
        "self_attested_attributes": {},
        "requested_attributes": {},
        "requested_predicates": {},
    }

    return Response("some_data")


def handle_get_active_menu(message):
    # TODO add/update issuer info?
    print("handle_get_active_menu()", message)
    return Response("")


def handle_perform_menu_action(message):
    # TODO add/update issuer info?
    print("handle_perform_menu_action()", message)
    return Response("")


def handle_register_issuer(message):
    """Handles the registration of a new issuing agent in the credential registry.
       
       The agent registration credential will be in the following format:
       {
            "issuer_registration_id": "string",
            "connection_id": "string",
            "issuer_registration": {
                "credential_types": [
                {
                    "category_labels": ["string"],
                    "claim_descriptions": ["string"],
                    "credential_def_id": "string",
                    "name": "string",
                    "credential": "string",
                    "topic": "string",
                    "endpoint": "string",
                    "cardinality_fields": [{}],
                    "mapping": {},
                    "version": "string",
                    "visible_fields": ["string"],
                    "description": "string",
                    "logo_b64": "string",
                    "schema": "string",
                    "claim_labels": ["string"]
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
            },
            "initiator": "self",
            "state": "registration_sent"
        }
    """
    issuer_manager = IssuerManager()
    updated = issuer_manager.register_issuer(message)
    return Response(content_type="application/json", data={"result": updated})
