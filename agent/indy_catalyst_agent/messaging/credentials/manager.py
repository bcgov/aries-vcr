"""Classes to manage credentials."""

import logging

from ..request_context import RequestContext
from ...error import BaseError


class CredentialManagerError(BaseError):
    """Credential error."""


class CredentialManager:
    """Class for managing credentials."""

    def __init__(self, context: RequestContext):
        """
        Initialize a CredentialManager.

        Args:
            context: The context for this credential
        """
        self._context = context
        self._logger = logging.getLogger(__name__)

    async def create_offer(self, credential_definition_id):

        pass


    async def receive_offer(self, credential_offer):

        pass

