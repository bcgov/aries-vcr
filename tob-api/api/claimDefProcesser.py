import asyncio
from api.indy.agent import Agent
from api.indy.claimDefParser import ClaimDefParser
import logging
from api.indy import eventloop

class ClaimDefProcesser(object):
  """
  Parses and processes a claim definition.

  _Currently only supports a 'Verified Organization' claim definition._
  """
  __orgbook = Agent()

  def __init__(self, claimDef) -> None:
    self.__logger = logging.getLogger(__name__)
    self.__claimDefParser = ClaimDefParser(claimDef)

  async def __StoreClaimOffer(self):
    self.__logger.debug("Storing claim offer ...")
    await self.__orgbook.store_claim_offer(self.__claimDefParser.did, self.__claimDefParser.seqNo)

  async def __StoreClaimRequest(self):
    self.__logger.debug("Storing claim request ...")
    return await self.__orgbook.store_claim_req(self.__claimDefParser.did, self.__claimDefParser.claimDefinition)

  async def __GenerateRequest(self):
    await self.__StoreClaimOffer()
    return await self.__StoreClaimRequest()

  def GenerateClaimRequest(self):
    return eventloop.do(self.__GenerateRequest())