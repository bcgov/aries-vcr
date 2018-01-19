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
    self.__logger.debug("Storing claim offer ...")
    async with Holder() as holder:
      await holder.store_claim_offer(
        self.__claimDefParser.did,
        self.__claimDefParser.seqNo
      )

  async def __StoreClaimRequest(self):
    self.__logger.debug("Storing claim request ...")
    async with Holder() as holder:
      return await holder.store_claim_req(
        self.__claimDefParser.did,
        self.__claimDefParser.claimDefinition
      )

  async def __GenerateRequest(self):
    await self.__StoreClaimOffer()
    return await self.__StoreClaimRequest()

  def GenerateClaimRequest(self):
    return eventloop.do(self.__GenerateRequest())
