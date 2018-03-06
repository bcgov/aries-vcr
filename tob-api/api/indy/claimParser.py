import os
import json
import logging
import requests

# LEDGER_URL = os.environ.get('LEDGER_URL')
# if not LEDGER_URL:
#     raise Exception('LEDGER_URL must be set.')


class ClaimParser(object):
    """
    Parses a generic claim.
    """
    def __init__(self, claim: str) -> None:
      self.__logger = logging.getLogger(__name__)
      self.__orgData = claim
      self.__parse()

    def __parse(self):
      self.__logger.debug("Parsing claim ...")
      data = json.loads(self.__orgData)
      self.__claim_type = data["claim_type"]
      self.__claim = data["claim_data"]
      self.__issuer_did = data["claim_data"]["issuer_did"]

      # # Get schema from ledger
      # # Once we upgrade to later version of
      # try:
      #   resp = requests.get('{}/ledger/domain/{}'.format(
      #       LEDGER_URL,
      #       self.__claim['schema_seq_no']
      #   ))
      #   self.__schema = resp.json()
      # except:
      #   self.__schema = None
    
    def getField(self, field):
      value = None
      try:
        value = self.__claim["values"][field][0]
      except:
        pass

      return value

    @property
    def schemaName(self) -> str:
        return self.__claim_type

    # @property
    # def schema(self) -> str:
    #     return self.__schema

    @property
    def issuerDid(self) -> str:
        return self.__issuer_did

    @property
    def json(self) -> str:
        return json.dumps(self.__claim)
