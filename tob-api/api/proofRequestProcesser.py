import json
from api.indy.agent import Agent
import logging
from api.indy import eventloop
from rest_framework.exceptions import NotAcceptable


class ProofRequestProcesser(object):
    """
    Parses a proof request and constructs a proof.

    Does not yet support predicates.
    """

    def __init__(self, proofRequestWithFilters) -> None:
        self.__orgbook = Agent()
        self.__logger = logging.getLogger(__name__)
        self.__proof_request = json.loads(proofRequestWithFilters)[
            'proof_request']
        self.__filters = json.loads(proofRequestWithFilters)['filters']

    async def __ConstructProof(self):
        self.__logger.debug("Constructing Proof ...")

        # We keep a reference to schemas that we discover and retrieve from the
        # ledger. We will need these again later.
        schemas = {}

        # The client is sending the proof request in an upcoming format.
        # This shim allows Permitify to declare its proof requests format
        # in the latest format. Once von-agent is update to support the new
        # format, this shim can be removed.
        for attr in self.__proof_request['requested_attrs']:
            # new format expects restrictions with "schema_key"
            # Current format simply wants the seq_no of schema
            schema_key = self.__proof_request['requested_attrs'][
                attr]['restrictions'][0]['schema_key']

            # Not optimal. von-agent should cache this.
            schema_json = await self.__orgbook.get_schema(
                schema_key['did'],
                schema_key['name'],
                schema_key['version']
            )
            schema = json.loads(schema_json)

            schemas[schema['seqNo']] = schema

            self.__proof_request['requested_attrs'][
                attr]['schema_seq_no'] = schema['seqNo']
            del self.__proof_request['requested_attrs'][attr]['restrictions']

        self.__logger.debug(self.__proof_request)

        # Get claims for proof request from wallet
        claims = await self.__orgbook.get_claims(
            json.dumps(self.__proof_request))
        claims = json.loads(claims[1])

        # If any of the claims for proof are empty, we cannot construct a proof
        for attr in claims['attrs']:
            if not claims['attrs'][attr]:
                raise NotAcceptable('No claims found for attr')

        def get_claim_by_filter(clms, key, value):
            for clm in clms:
                if clm["attrs"][key] == value:
                    return clm
            raise NotAcceptable('No claims found for filter')

        requested_claims = {
            'self_attested_attributes': {},
            'requested_attrs': {
                attr: [
                    # Either we get the first claim found
                    # by the provided filter
                    get_claim_by_filter(
                        claims["attrs"][attr],
                        attr,
                        self.__filters[attr])["claim_uuid"]
                    # Or we use the first claim found
                    if attr in self.__filters[attr]
                    else claims["attrs"][attr][0]["claim_uuid"],
                    True
                ]
                for attr in claims["attrs"]
            },
            'requested_predicates': {}
        }

        # Build schemas json
        schemas = {
            claims["attrs"][attr][0]['claim_uuid']: schemas[claims["attrs"][attr][0]["schema_seq_no"]]
            for attr in claims["attrs"]
        }

        claim_defs = {
            claims["attrs"][attr][0]['claim_uuid']: json.loads(eventloop.do(
                self.holder.get_claim_def(
                    claims["attrs"][attr][0]["schema_seq_no"],
                    claims["attrs"][attr][0]["issuer_did"]
                )
            ))
            for attr in claims["attrs"]
        }

        proof = await self.holder.create_proof(
                json.dumps(self.__proof_request),
                json.dumps(schemas),
                json.dumps(claim_defs),
                requested_claims
            )

        return proof

    def ConstructProof(self):
        return eventloop.do(self.__ConstructProof())
