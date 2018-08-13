import json
import logging
from collections import namedtuple

from von_agent import util as von_agent_util

from api.indy.agent import Holder
from api.indy import eventloop

from api_v2.models.Schema import Schema
from api_v2.models.Issuer import Issuer
from api_v2.models.CredentialType import CredentialType


logger = logging.getLogger(__name__)


Filter = namedtuple("Filter", "claim_name claim_value")


class ProofException(Exception):
    pass


class ProofManager(object):
    """
    Class to manage creation of indy proofs.
    """

    def __init__(self, proof_request: dict) -> None:
        """Constructor
        
        Arguments:
            proof_request {dict} -- valid indy proof request
        """

        self.proof_request = proof_request
        self.filters = []

    def add_filter(self, claim_name: str, claim_value: str):
        self.filters.append(Filter(claim_name, claim_value))

    def construct_proof(self):
        return eventloop.do(self.construct_proof_async())

    async def construct_proof_async(self):
        async with Holder() as holder:
            try:
                credential_ids = set(
                    [
                        self.proof_request["requested_attributes"][attribute][
                            "credential_id"
                        ]
                        for attribute in self.proof_request[
                            "requested_attributes"
                        ]
                    ]
                )
            except KeyError as error:
                raise ProofException(
                    "Proof requests must specify credential_id"
                )
            else:
                credentials_for_proof_request = await holder.get_creds_by_id(
                    json.dumps(self.proof_request), credential_ids
                )

            # We get creds by id for now instead of by restrictions key
            # referents, credentials_for_proof_request = await holder.get_creds(
            #     json.dumps(self.proof_request)
            # )

            credentials_for_proof_request = json.loads(
                credentials_for_proof_request
            )

            # Construct the required payload to create proof
            requested_credentials = {}
            requested_credentials["self_attested_attributes"] = {}
            requested_credentials["requested_predicates"] = {}
            requested_credentials["requested_attributes"] = {}

            for referent_name in credentials_for_proof_request["attrs"]:
                requested_credentials["requested_attributes"][referent_name] = {}
                requested_credentials["requested_attributes"][referent_name][
                    "revealed"
                ] = True

                # Get the credential_id for this claim from proof request
                (credential_id,) = [
                    self.proof_request["requested_attributes"][attr][
                        "credential_id"
                    ]
                    for attr in self.proof_request["requested_attributes"]
                    if attr == referent_name
                ]

                requested_credentials["requested_attributes"][referent_name][
                    "cred_id"
                ] = credential_id

            proof = await holder.create_proof(
                self.proof_request,
                credentials_for_proof_request,
                requested_credentials,
            )

            return json.loads(proof)
