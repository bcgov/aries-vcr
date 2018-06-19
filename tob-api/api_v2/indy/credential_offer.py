import json
import logging

from api.indy.agent import Holder
from api.indy import eventloop

logger = logging.getLogger(__name__)


class CredentialOfferManager(object):
    """
    Handles credential offer from issuer.
    """
    def __init__(self, credential_offer, credential_definition) -> None:
        self.credential_offer = credential_offer
        self.credential_definition = credential_definition

    def generate_credential_request(self):
        """Generates a credential request
        
        Returns:
            tuple -- credential_request, credential_request_metadata
        """
        async def run():
            async with Holder() as holder:
                (
                    credential_request,
                    credential_request_metadata_json,
                ) = await holder.create_cred_req(
                    json.dumps(self.credential_offer),
                    json.dumps(self.credential_definition),
                )
            return credential_request, json.loads(
                credential_request_metadata_json
            )

        return eventloop.do(run())
