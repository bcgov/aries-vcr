import os
import json
import logging
import requests


class ClaimParser(object):
    """
    Parses a generic claim.
    """

    def __init__(self, claim: str) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__orgData = claim
        self.__parse()

    def __parse(self):
        self.__logger.debug(
            "\n============================================================================\n"
            + "Parsing claim:\n"
            + "----------------------------------------------------------------------------\n"
            + "{0}\n".format(json.dumps(json.loads(self.__orgData), indent=2))
            + "============================================================================\n"
        )

        data = json.loads(self.__orgData)
        self.__claim_type = data["claim_type"]
        self.__data = data["claim_data"]
        self.__issuer_did = data["issuer_did"]
        self.__cred_def = data["cred_def"]
        self.__cred_req_metadata = data["cred_req_metadata"]

    def getField(self, field):
        value = None
        try:
            value = self.__data["values"][field]["raw"]
        except Exception:
            pass

        return value

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def schemaName(self) -> str:
        return self.__claim_type

    @property
    def issuerDid(self) -> str:
        return self.__issuer_did

    @property
    def credDef(self) -> str:
        return self.__cred_def

    @property
    def credReqMeta(self) -> str:
        return self.__cred_req_metadata

    @property
    def json(self) -> str:
        return json.dumps(self.__data)
