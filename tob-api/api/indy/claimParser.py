import json

class ClaimParser(object):
    """
    description of class
    """
    def __init__(self, claim: str) -> None:
        """
        Initializer
        """
        self._raw_claim = claim
        self.__parse()

    @property
    def raw_claim(self) -> str:
        return self._raw_claim

    @property
    def claim(self) -> str:
        return self._claim

    @property
    def issuer_did(self) -> str:
        return self._issuer_did

    def __parse(self):
      data = json.loads(self.raw_claim)
      self._issuer_did = data["issuer_did"]
      self._claim = self.__parseClaim(data)

    def __parseClaim(self, data):
      return {
        "effectiveDate": data["claim"]["effectiveDate"][0],
        "orgTypeId": data["claim"]["orgTypeId"][0],
        "endDate": data["claim"]["endDate"][0],
        "jurisdictionId": data["claim"]["jurisdictionId"][0],
        "LegalName": data["claim"]["LegalName"][0],
        "busId": data["claim"]["busId"][0]
      }
      

