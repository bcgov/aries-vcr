"""Classes to manage credentials."""

import logging

from ...error import BaseError
from ..request_context import RequestContext


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

    async def send_credential_offer(self, connection_record, credential_definition_id):
        """
        Send a credential offer to a connection.

        Args:
            connection_record: The connection to send the credential offer to
            credential_definition_id: The id for the credential definition to issue
                the credential against

        """

        
