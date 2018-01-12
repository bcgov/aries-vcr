import json
import logging

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
    
    def getField(self, field):
      return self.__claim["claim"][field][0]

    @property
    def claimType(self) -> str:
        return self.__claim_type

    @property
    def issuerDid(self) -> str:
        return self.__issuer_did

    @property
    def json(self) -> str:
        return json.dumps(self.__claim)