import json

class ClaimParser(object):
    """
    Parses a claim.
    _Currently only supports 'Verified Organization' claims._
    """
    def __init__(self, claim: str) -> None:
        self.__raw_claim = claim
        self.__data = json.loads(self.rawClaim)
        self.__parse()

    @property
    def rawClaim(self) -> str:
        return self.__raw_claim

    @property
    def fullClaim(self) -> str:
        return self.__data

    @property
    def claim(self) -> str:
        return self.__claim

    @property
    def issuerDid(self) -> str:
        return self.__issuer_did

    def __parse(self):
      self.__issuer_did = self.fullClaim["issuer_did"]
      self.__claim = self.__parseClaim()

    def __parseClaim(self):
      return {
        "effectiveDate": self.fullClaim["claim"]["effectiveDate"][0],
        "orgTypeId": self.fullClaim["claim"]["orgTypeId"][0],
        "endDate": self.fullClaim["claim"]["endDate"][0],
        "jurisdictionId": self.fullClaim["claim"]["jurisdictionId"][0],
        "LegalName": self.fullClaim["claim"]["LegalName"][0],
        "busId": self.fullClaim["claim"]["busId"][0]
      }
      

