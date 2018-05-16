import json
import asyncio
from api.indy.agent import Holder
from api.indy.claimDefParser import ClaimDefParser
import logging
from api.indy import eventloop


class ClaimDefProcesser(object):
    """
    Parses and processes a claim definition.
    """

    def __init__(self, claimDef) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__claimDefParser = ClaimDefParser(claimDef)

    async def __StoreClaimRequest(self):
        self.__logger.debug(">>> Storing claim request ...")
        async with Holder() as holder:
            (credential_request, credential_request_metadata_json) = await holder.create_cred_req(
                self.__claimDefParser.claimOffer,
                self.__claimDefParser.claimDefinition
            )
        self.__logger.debug("<<< Storing claim request.")
        return (credential_request, json.loads(credential_request_metadata_json))

    async def __GenerateRequest(self):
        self.__logger.debug("Generating claim request ...")
        (credential_request, credential_request_metadata) = await self.__StoreClaimRequest()

        self.__logger.debug(
            "\n============================================================================\n" +
            "Claim request generated:\n" +
            "----------------------------------------------------------------------------\n" +
            "{0}\n".format(json.dumps(json.loads(credential_request), indent=2)) +
            "============================================================================\n")

        return (credential_request, credential_request_metadata)

    def GenerateClaimRequest(self):
        return eventloop.do(self.__GenerateRequest())
