from api.indy.agent import Agent
import logging
from api.indy import eventloop

class ProofRequestProcesser(object):
  """
  Parses a proof request and constructs a proof.
  """

  def __init__(self, proofRequestWithFilters) -> None:
    self.__orgbook = Agent()
    self.__logger = logging.getLogger(__name__)
    self.__proof_request = proofRequestWithFilters['proof_request']
    self.__filters = proofRequestWithFilters['filters']

  async def __ConstructProof(self):
    self.__logger.debug("Constructing Proof ...")
    return { "test": "A" }

  def ConstructProof(self):
    return eventloop.do(self.__ConstructProof())
