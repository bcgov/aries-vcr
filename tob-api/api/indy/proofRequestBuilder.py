import json
from random import randrange


class ProofRequestBuilder(object):
    """
    Utility to construct a proof request programmatically
    """
    def __init__(self, name, version) -> None:
        self.__name = name
        self.__version = version
        self.__nonce = randrange(0, 99999999)
        self.__requestedAttrs = {}

    @property
    def nonce(self) -> int:
        return self.__nonce

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    def asDict(self):
        proofRequest = {
            'name': self.__name,
            'version': self.__version,
            'nonce': str(self.__nonce),
            'requested_attrs': self.__requestedAttrs,
            'requested_predicates': {} # Not yet supported
        }

        return proofRequest

    def addRequestedAttr(self, name, restrictions):
        self.__requestedAttrs[name] = {
            'name': name,
            'restrictions': restrictions
        }

    def matchCredential(
            self,
            claimJson,
            schemaName,
            schemaVersion):
        """
        Creates a proof request from a credential
        """

        claim = json.loads(claimJson)
        issuerDid = claim['issuer_did']

        # Extract attrs from claim
        parsedClaimAttrs = [attr for attr in claim['claim']]

        for attr in parsedClaimAttrs:
            self.addRequestedAttr(attr, [{
                "schema_key": {
                    "did": issuerDid,
                    "name": schemaName,
                    "version": schemaVersion
                }
            }])
