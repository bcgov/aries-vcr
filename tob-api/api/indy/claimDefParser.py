import json

class ClaimDefParser(object):
    """
    Parses a claim definition.
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
    def claimOffer(self) -> str:
        return self.__claim_offer

    def __parse(self):
      self.__claim_offer = self.fullClaimDefinition["claim_offer"]
      self.__claim_def = self.fullClaimDefinition["claim_def"]