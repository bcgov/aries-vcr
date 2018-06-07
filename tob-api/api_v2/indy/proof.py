import logging

logger = logging.getLogger(__name__)


class ProofManager(object):
    def __init__(self, proof_request) -> None:
        self.proof_request = proof_request
