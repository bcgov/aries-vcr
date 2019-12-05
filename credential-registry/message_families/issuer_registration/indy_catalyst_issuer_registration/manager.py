"""Classes to manage issuer registrations."""

import logging

from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.error import BaseError

from .models.issuer_registration_state import IssuerRegistrationState
from .messages.register import IssuerRegistration


class IssuerRegistrationManagerError(BaseError):
    """Issuer registration error."""


class IssuerRegistrationManager:
    """Class for managing issuer registrations."""

    def __init__(self, context: InjectionContext):
        """
        Initialize a IssuerRegistrationManager.

        Args:
            context: The context for this issuer registration
        """
        self._context = context
        self._logger = logging.getLogger(__name__)

    @property
    def context(self) -> InjectionContext:
        """
        Accessor for the current injection context.

        Returns:
            The injection context for this connection

        """
        return self._context

    async def prepare_send(self, connection_id: str, issuer_registration: dict):
        """
        Create an issuer registration state object and agent messages.

        Args:
            connection_id: Connection to send the issuer registration to
            issuer_registration: The issuer registration payload

        Returns:
            A tuple (
                issuer_registration_state,
                issuer_registration_message
            )

        """

        issuer_registration_message = IssuerRegistration(
            issuer_registration=issuer_registration
        )

        issuer_registration_state = IssuerRegistrationState(
            connection_id=connection_id,
            initiator=IssuerRegistrationState.INITIATOR_SELF,
            state=IssuerRegistrationState.STATE_REGISTRATION_SENT,
            issuer_registration=issuer_registration,
        )
        await issuer_registration_state.save(self.context)

        return issuer_registration_state, issuer_registration_message

    async def receive_registration(
        self, connection_id: str, issuer_registration_message: dict
    ):
        """
        Receive an issuer registration message.

        Args:
            connection_id: Connection to send the issuer registration to
            issuer_registration: The issuer registration payload

        Returns:
            Issuer registration state object


        """

        issuer_registration_state = IssuerRegistrationState(
            connection_id=connection_id,
            thread_id=issuer_registration_message._thread_id,
            initiator=IssuerRegistrationState.INITIATOR_EXTERNAL,
            state=IssuerRegistrationState.STATE_REGISTRATION_RECEIVED,
            issuer_registration=issuer_registration_message.issuer_registration,
        )
        await issuer_registration_state.save(self.context)

        return issuer_registration_state
