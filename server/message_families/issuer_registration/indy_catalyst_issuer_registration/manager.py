"""Classes to manage issuer registrations."""

import logging
from typing import Tuple

from aries_cloudagent.core.error import BaseError
from aries_cloudagent.core.profile import ProfileSession

from .models.issuer_registration_state import IssuerRegistrationState
from .messages.register import IssuerRegistration


class IssuerRegistrationManagerError(BaseError):
    """Issuer registration error."""


class IssuerRegistrationManager:
    """Class for managing issuer registrations."""

    def __init__(self, session: ProfileSession):
        """
        Initialize a IssuerRegistrationManager.

        Args:
            session: The session for this issuer registration
        """
        self._session = session
        self._logger = logging.getLogger(__name__)

    @property
    def session(self) -> ProfileSession:
        """
        Accessor for the current injection session.

        Returns:
            The injection session for this connection

        """
        return self._session

    async def prepare_send(
        self, connection_id: str, issuer_registration: dict
    ) -> Tuple[IssuerRegistrationState, IssuerRegistration]:
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
            state=None,
            issuer_registration=issuer_registration,
        )
        await issuer_registration_state.save(self.session)

        return issuer_registration_state, issuer_registration_message

    async def receive_registration(
        self, connection_id: str, issuer_registration_message: dict
    ) -> IssuerRegistrationState:
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
            state=None,
            issuer_registration=issuer_registration_message.issuer_registration,
        )
        await issuer_registration_state.save(self.session)

        return issuer_registration_state
