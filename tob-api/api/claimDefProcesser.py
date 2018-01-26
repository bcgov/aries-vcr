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

  async def __StoreClaimOffer(self):
    self.__logger.debug(">>> Storing claim offer ...")
    async with Holder() as holder:
      await holder.store_claim_offer(
        self.__claimDefParser.did,
        self.__claimDefParser.seqNo
      )
    self.__logger.debug("<<< Storing claim offer.")


  async def __StoreClaimRequest(self):
    self.__logger.debug(">>> Storing claim request ...")
    async with Holder() as holder:
      claim_request = await holder.store_claim_req(
        self.__claimDefParser.did,
        self.__claimDefParser.claimDefinition
      )
    self.__logger.debug("<<< Storing claim request.")
    return claim_request

  async def __GenerateRequest(self):
    self.__logger.debug("Generating claim request ...")
    await self.__StoreClaimOffer()
    claim_request = await self.__StoreClaimRequest()

    self.__logger.debug(
      "\n============================================================================\n" +
      "Claim request generated:\n" +
      "----------------------------------------------------------------------------\n" +
      "{0}\n".format(json.dumps(json.loads(claim_request), indent=4)) +
      "============================================================================\n")

    return claim_request

  def GenerateClaimRequest(self):
    return eventloop.do(self.__GenerateRequest())
