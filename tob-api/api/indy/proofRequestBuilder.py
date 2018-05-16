import json
from random import randrange
import logging


class ProofRequestBuilder(object):
    """
    Utility to construct a proof request programmatically
    """

    def __init__(self, name, version) -> None:
        self.__name = name
        self.__version = version
        self.__nonce = randrange(0, 99999999)
        self.__requestedAttrs = {}
        self.__logger = logging.getLogger(__name__)

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
            'requested_attributes': self.__requestedAttrs,
            'requested_predicates': {}  # Not yet supported
        }

        self.__logger.debug(
            "\n============================================================================\n" +
            "Emitting proof request as dict:\n" +
            "----------------------------------------------------------------------------\n" +
            "{0}\n".format(json.dumps(proofRequest, indent=2)) +
            "============================================================================\n")

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
            schemaVersion,
            issuerDid):
        """
        Creates a proof request from a credential
        """

        claim = json.loads(claimJson)

        self.__logger.debug(
            "\n============================================================================\n" +
            "Creating proof request from credential:\n" +
            "----------------------------------------------------------------------------\n" +
            "{0}\n".format(json.dumps(claim, indent=2)) +
            "============================================================================\n")

        # Extract attrs from claim
        parsedClaimAttrs = [attr for attr in claim['values']]

        for attr in parsedClaimAttrs:

            self.__logger.debug(
                "\n============================================================================\n" +
                "Adding {} restriction to proof request:\n".format(attr) +
                "----------------------------------------------------------------------------\n" +
                "{}\n".format(json.dumps({
                    "issuer_did": issuerDid,
                    "schema_name": schemaName,
                    "schema_version": schemaVersion
                }, indent=2)) +
                "============================================================================\n")

            self.addRequestedAttr(attr, [{
                "issuer_did": issuerDid,
                "schema_name": schemaName,
                "schema_version": schemaVersion
            }])
