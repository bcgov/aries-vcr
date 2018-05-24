import os
import json

from indy import anoncreds
from api.indy.agent import Holder
import logging
from api.indy import eventloop
from rest_framework.exceptions import NotAcceptable
import requests
import time

# LEDGER_URL = os.environ.get('LEDGER_URL')
# if not LEDGER_URL:
#     raise Exception('LEDGER_URL must be set.')


class ProofRequestProcesser(object):
    """
    Parses a proof request and constructs a proof.

    Does not yet support predicates.
    """

    def __init__(self, proofRequestWithFilters) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__proof_request = json.loads(proofRequestWithFilters)[
            'proof_request']
        self.__filters = json.loads(proofRequestWithFilters)['filters'] \
            if 'filters' in json.loads(proofRequestWithFilters) \
            else {}

    async def __ConstructProof(self):
        self.__logger.debug("Constructing Proof ...")

        # # We keep a reference to schemas that we discover and retrieve from the
        # # ledger. We will need these again later.
        # schema_cache = {'by_key': {}}

        # # The client is sending the proof request in an upcoming format.
        # # This shim allows Permitify to declare its proof requests format
        # # in the latest format. Once von-agent is update to support the new
        # # format, this shim can be removed.
        # for attr in self.__proof_request['requested_attrs']:
        #     # new format expects restrictions with "schema_key"
        #     # Current format simply wants the seq_no of schema
        #     schema_key = self.__proof_request['requested_attrs'][
        #         attr]['restrictions'][0]['schema_key']

        #     # This is offensive...
        #     # Get the schema from the ledger directly by name/version
        #     # After upgrading von-agent we can loosen restrictions using
        #     # schema_key
        #     # try:
        #     #     for line in self.ledger.splitlines():
        #     #         entry = json.loads(line)[1]
        #     #         if entry['type'] == "101":
        #     #             if entry['data']['name'] == schema_key['name'] and \
        #     #                     entry['data']['version'] == schema_key['version']:
        #     #                 schema_key['did'] = entry['identifier']
        #     #                 break
        #     # except:
        #     #     raise Exception('Could not correlate schema name and version to did.')

        #     # Ugly cache for now...
        #     if '%s::%s::%s' % (
        #             schema_key['did'],
        #             schema_key['name'],
        #             schema_key['version']) in schema_cache['by_key']:
        #         schema = schema_cache['by_key']['%s::%s::%s' % (
        #             schema_key['did'],
        #             schema_key['name'],
        #             schema_key['version'])]
        #     else:
        #         # Not optimal. von-agent should cache this.
        #         async with Holder() as holder:
        #             schema_json = await holder.get_schema(
        #                 schema_key['did'],
        #                 schema_key['name'],
        #                 schema_key['version']
        #             )
        #             schema = json.loads(schema_json)

        #     self.__logger.debug("Using Schema key {}".format(schema_key))

        #     if not schema:
        #         raise NotAcceptable(
        #             'No schema found for did:{} name:{} version:{}'.format(
        #                 schema_key['did'],
        #                 schema_key['name'],
        #                 schema_key['version']
        #             )
        #         )

        #     schema_cache[schema['seqNo']] = schema
        #     schema_cache['by_key']['%s::%s::%s' % (
        #         schema_key['did'],
        #         schema_key['name'],
        #         schema_key['version'])] = schema

        #     self.__proof_request['requested_attrs'][
        #         attr]['schema_seq_no'] = schema['seqNo']
        #     del self.__proof_request['requested_attrs'][attr]['restrictions']

        # self.__logger.debug('Schema cache: %s' % json.dumps(schema_cache))

        self.__logger.debug('Proof request: %s' % json.dumps(
            self.__proof_request))

        # legal entity id
        self.__logger.debug(self.__filters)
        if 'legal_entity_id' in self.__filters:
            legal_entity_id = self.__filters['legal_entity_id']
            self.__logger.debug(
                'Proof request for legal_entity_id: %s' % legal_entity_id)
        else:
            legal_entity_id = None
            self.__logger.debug(
                'Proof request for legal_entity_id: None found')

        # Get claims for proof request from wallet
        async with Holder(legal_entity_id) as holder:
            # claims = await anoncreds.prover_get_credentials_for_proof_req(holder.wallet.handle, json.dumps(self.__proof_request))
            claims = await holder.get_creds(
                json.dumps(self.__proof_request))

            self.__logger.debug(
                '\n\nholder.get_creds result:\n\n {}'.format(claims))
            claims = json.loads(claims[1])

        self.__logger.debug(
            'Wallet returned the following claims for proof request: %s' %
            json.dumps(claims))

        # If any of the claims for proof are empty, we cannot construct a proof
        for attr in claims['attrs']:
            if not claims['attrs'][attr]:
                raise NotAcceptable('No claims found for attr %s' % attr)

        def get_claim_by_filter(clms, key, value):
            for clm in clms:
                if clm["cred_info"]["attrs"][key] == value:
                    return clm
            raise NotAcceptable(
                'No claims found for filter %s = %s' % (
                    key, value))

        # TODO: rework to support other filters other than legal_entity_id
        requested_claims = {
            'self_attested_attributes': {},
            'requested_attributes': {
                attr: {
                    'cred_id': get_claim_by_filter(
                        claims["attrs"][attr],
                        'legal_entity_id',
                        self.__filters['legal_entity_id'])["cred_info"]["referent"]
                    # Or we use the first claim found
                    if 'legal_entity_id' in self.__filters
                    else claims["attrs"][attr][0]["cred_info"]["referent"],
                    'revealed': True
                }
                for attr in claims["attrs"]
            },
            'requested_predicates': {}
        }

        self.__logger.debug(
            'Built requested claims: %s' %
            json.dumps(requested_claims))

        # Build schemas json
        def wallet_claim_by_referent(clms, referent):
            for clm in clms:
                if clm['referent'] == referent:
                    return clm

        # schemas = {
        #     requested_claims['requested_attrs'][attr][0]:
        #         schema_cache[
        #             wallet_claim_by_referent(
        #                 claims["attrs"][attr],
        #                 requested_claims['requested_attrs'][attr][0]
        #             )['schema_seq_no']
        #         ]
        #     for attr in requested_claims['requested_attrs']
        # }

        # self.__logger.debug(
        #     'Built schemas: %s' %
        #     json.dumps(schemas))

        # claim_defs_cache = {}
        # claim_defs = {}
        # for attr in requested_claims['requested_attrs']:
        #     # claim uuid
        #     referent = requested_claims['requested_attrs'][attr][0]

        #     if referent not in claim_defs_cache:
        #         async with Holder() as holder:
        #             claim_defs_cache[referent] = \
        #                 json.loads(await holder.get_claim_def(
        #                     wallet_claim_by_referent(
        #                         claims["attrs"][attr],
        #                         referent
        #                     )["schema_seq_no"],
        #                     wallet_claim_by_referent(
        #                         claims["attrs"][attr],
        #                         referent
        #                     )["issuer_did"]
        #                 ))

        #     claim_defs[referent] = claim_defs_cache[referent]

        # self.__logger.debug(
        #     'Claim def cache: %s' %
        #     json.dumps(claim_defs_cache))

        # self.__logger.debug(
        #     'Built claim_defs: %s' %
        #     json.dumps(claim_defs))

        self.__logger.debug("Creating proof ...")

        # A shim to remove unrelated claims from
        # response from wallet.
        for attr in requested_claims['requested_attributes']:
            claim_uuid = requested_claims['requested_attributes'][attr]["cred_id"]
            claim_attrs = claims['attrs'][attr]

            # We iterate through claims and remove
            # any claims we don't want
            for claim_attr in claim_attrs:
                if claim_attr["cred_info"]['referent'] == claim_uuid:
                    claims['attrs'][attr] = [claim_attr]

        self.__logger.debug('-=-=-=-=-=-==-\n\n\n\n')
        self.__logger.debug(json.dumps(claims, indent=2))
        self.__logger.debug(json.dumps(requested_claims, indent=2))
        self.__logger.debug('-=-=-=-=-=-==-\n\n\n\n')

        async with Holder(legal_entity_id) as holder:
            proof = await holder.create_proof(
                self.__proof_request,
                claims,
                requested_claims
            )
            elapsed_time = time.time() - start_time
            self.__logger.debug(
                'Proof elapsed time >>> {}'.format(elapsed_time))

        self.__logger.debug(
            'Created proof: %s' %
            json.dumps(proof))

        return {
            'proof': json.loads(proof)
        }

    def ConstructProof(self):
        return eventloop.do(self.__ConstructProof())
