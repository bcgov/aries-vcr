import json

class ClaimDefParser(object):
    """
    Parses a claim definition.
    _Currently only supports 'Verified Organization' claim definitions._
    """
    def __init__(self, claimRequest: str) -> None:
        """
        Initializer
        """
        self.__raw_claim_def = claimRequest
        self.__data = json.loads(self.rawClaimDefinition)
        self.__parse()

    @property
    def rawClaimDefinition(self) -> str:
        return self.__raw_claim_def

    @property
    def fullClaimDefinition(self) -> str:
        return self.__data

    @property
    def claimDefinition(self) -> str:
        return self.__claim_def

    @property
    def did(self) -> str:
        return self.__did

    @property
    def seqNo(self) -> str:
        return self.__seqNo

    def __parse(self):
      self.__did = self.fullClaimDefinition["did"]
      self.__seqNo = self.fullClaimDefinition["seqNo"]
      self.__claim_def = self.fullClaimDefinition["claim_def"]