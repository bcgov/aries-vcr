import os
import logging

import requests

from django.conf import settings
from icat_hooks.celery import app

from icat_cbs.utils.credential import Credential, CredentialManager

LOGGER = logging.getLogger(__name__)

@app.task
def handle_credential(state, message):
    # global admin_url

    credential_exchange_id = message["credential_exchange_id"]
    LOGGER.info(
        f"Processing credential. state={state}, credential_exchange_id={credential_exchange_id}"
    )

    try:
        if state == "offer_received":
            print("After receiving credential offer, send credential request")
            # resp = requests.post(admin_url + '/credential_exchange/' + credential_exchange_id + '/send-request')
            # assert resp.status_code == 200
            return

        elif state == "credential_received":
            raw_credential = message["raw_credential"]

            # print("Received credential:")
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

            return

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

