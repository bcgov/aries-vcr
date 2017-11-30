import json

# ToDo:
# * The code, currently, only supports a single claim type; a 'Verified Organization' claim.

class ClaimParser(object):
    """
    description of class
    """
    def __init__(self, claim: str) -> None:
        """
        Initializer
        """
        self._raw_claim = claim
        self._data = json.loads(self.rawClaim)
        self.__parse()

    @property
    def rawClaim(self) -> str:
        return self._raw_claim

    @property
    def fullClaim(self) -> str:
        return self._data

    @property
    def claim(self) -> str:
        return self._claim

    @property
    def issuerDid(self) -> str:
        return self._issuer_did

    def __parse(self):
      self._issuer_did = self.fullClaim["issuer_did"]
      self._claim = self.__parseClaim()

    def __parseClaim(self):
      return {
        "effectiveDate": self.fullClaim["claim"]["effectiveDate"][0],
        "orgTypeId": self.fullClaim["claim"]["orgTypeId"][0],
        "endDate": self.fullClaim["claim"]["endDate"][0],
        "jurisdictionId": self.fullClaim["claim"]["jurisdictionId"][0],
        "LegalName": self.fullClaim["claim"]["LegalName"][0],
        "busId": self.fullClaim["claim"]["busId"][0]
      }
      

