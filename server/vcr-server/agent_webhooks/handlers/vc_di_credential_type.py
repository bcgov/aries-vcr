import logging

from marshmallow import ValidationError

from agent_webhooks.enums import FormatEnum
from agent_webhooks.schemas import CredentialTypeRegistrationDefSchema

from agent_webhooks.utils.issuer import IssuerManager, IssuerRegistrationResult

LOGGER = logging.getLogger(__name__)

format = FormatEnum.VC_DI.value


def handle_credential_type(
    message: CredentialTypeRegistrationDefSchema,
) -> IssuerRegistrationResult:
    f"""Webhook message handler for a {format} credential type."""

    try:
        credential_type_registration_schema = CredentialTypeRegistrationDefSchema()
        credential_type_registration_schema.load(message)
        issuer_registration_def = credential_type_registration_schema.dump(message)
        issuer_manager = IssuerManager()

        return issuer_manager.register_issuer(issuer_registration_def)
    except ValidationError as err:
        LOGGER.error(f"Invalid {format} credential type definition: {err.messages}")
        raise err
    except Exception as err:
        LOGGER.error(f"Error handling {format} credential type webhook: {err}")
        raise err
