import logging

import requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from icat_cbs.utils.credential import Credential, CredentialManager
from icat_cbs.utils.issuer import IssuerManager

from api_v2.models.Credential import Credential as CredentialModel

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

            credential = Credential(credential_data)

            credential_manager = CredentialManager()
            credential = credential_manager.process(credential)

            # Instruct the agent to store the credential in wallet
            resp = requests.post(
                f"{settings.AGENT_ADMIN_URL}/credential_exchange/{credential_exchange_id}/store",
                json={"credential_id": credential.credential_id},
                headers=settings.ADMIN_REQUEST_HEADERS,
            )
            resp.raise_for_status()

            return Response({"success": True})

        # TODO other scenarios
        elif state == "stored":
            print("credential stored")
            # print(message)

    except Exception as e:
        LOGGER.error(str(e))
        # Send a problem report for the error
        resp = requests.post(
            f"{settings.AGENT_ADMIN_URL}/credential_exchange/{credential_exchange_id}/problem_report",
            json={"explain_ltxt": str(e)},
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        resp.raise_for_status()
        return Response({"success": False, "error": str(e)})

    return Response("")


def handle_presentations(state, message):
    print("handle_presentations()", state, message)

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

        resp = requests.get(
            f"{settings.AGENT_ADMIN_URL}/presentation_exchange/"
            + f"{message['presentation_exchange_id']}/credentials/"
            + f"{referents}"
        )

        # All credentials from wallet that satisfy presentation request
        credentials = resp.json()

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

        # Now we need to provide a credential id for each requested_*
        for credential in credentials:
            # This query plus limiting by claim values below
            # *should* return exactly one result
            credential_query = CredentialModel.objects.filter(
                revoked=False, inactive=False, latest=True
            )
            for attr in credential["cred_info"]["attrs"]:
                credential_query = credential_query.filter(
                    claims__name=attr,
                    claims__value=credential["cred_info"]["attrs"][attr],
                )

            # If we don't have exactly 1 result, we can't construct a presentation
            # deterministically
            results_length = len(credential_query)
            if results_length != 1:
                raise Exception(
                    "Number of credentials returned by query "
                    + f"{credential_query.query} was not 1, it was {results_length}"
                )

            # Since we have the credential_exchange id stored on the credential
            # we need to call out to get the credential_id for this credential_exchange
            # (This is added after we process the credential and it is stored in
            # the agent's wallet)
            credential_result = credential_query.first()
            credential_exchange_id = credential_result.credential_exchange_id
            resp = requests.get(
                f"{settings.AGENT_ADMIN_URL}/credential_exchange/{credential_exchange_id}"
            )
            credential_exchange_object = resp.json()

            credential_id = credential_exchange_object["credential_id"]

            # Ensure that the credential_id we retrieved from the agent is in fact
            # in the set of credentials returned from the wallet in the first place.
            # This should be true.
            assert credential_id in [
                credential["cred_info"]["referent"] for credential in credentials
            ]

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
            f"{settings.AGENT_ADMIN_URL}/presentation_exchange/"
            + f"{presentation_exchange_id}/send_presentation",
            json=credentials_for_presentation,
        )

        resp.raise_for_status()

    return Response()


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

    for cred_def_id, tag_attrs in tag_policy_updates.items():
        # instruct the agent to update the tag policy
        resp = requests.post(
            f"{settings.AGENT_ADMIN_URL}/wallet/tag-policy/{cred_def_id}",
            json={"taggables": list(tag_attrs)},
            headers=settings.ADMIN_REQUEST_HEADERS,
        )
        resp.raise_for_status()

    return Response(
        content_type="application/json", data={"result": updated.serialize()}
    )
