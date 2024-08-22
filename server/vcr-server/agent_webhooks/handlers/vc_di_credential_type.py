
import logging

from marshmallow import ValidationError

from agent_webhooks.enums import FormatEnum
from agent_webhooks.schemas import CredentialTypeRegistrationDefSchema

from agent_webhooks.utils.issuer import IssuerManager, IssuerRegistrationResult

LOGGER = logging.getLogger(__name__)

format = FormatEnum.VC_DI.value

def handle_credential_type(message: any) -> IssuerRegistrationResult:
    f"""Webhook message handler for a {format} credential type."""

    try:
        schema = CredentialTypeRegistrationDefSchema()
        schema.load(message)
        processed_message = schema.dump(message)
        issuer_manager = IssuerManager()

        # Note: Dangerous without proper validation
        issuer_def = {"issuer_registration": processed_message}
        return issuer_manager.register_issuer(issuer_def)
    except ValidationError as err:
        LOGGER.error(f"Invalid {format} credential type definition: {err.messages}")
        raise err
    except Exception as err:
        LOGGER.error(f"Error handling {format} credential type webhook: {err}")
        raise err
