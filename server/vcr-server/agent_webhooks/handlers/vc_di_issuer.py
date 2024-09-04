import logging

from marshmallow.exceptions import ValidationError

from agent_webhooks.enums import FormatEnum
from agent_webhooks.schemas import IssuerDefSchema, IssuerRegistrationDefSchema
from agent_webhooks.utils.issuer import IssuerManager, IssuerRegistrationResult

LOGGER = logging.getLogger(__name__)

format = FormatEnum.VC_DI.value


def handle_issuer(message: IssuerDefSchema) -> IssuerRegistrationResult:
    f"""Webhook message handler for a {format} issuer."""

    try:
        IssuerDefSchema().load(message)
        issuer_manager = IssuerManager()

        # Convert the issuer definition to an issuer registration definition
        issuer_registration_def = IssuerRegistrationDefSchema().dump({"issuer": message})
        return issuer_manager.register_issuer(issuer_registration_def, issuer_only=True)
    except ValidationError as err:
        LOGGER.error(f"Invalid {format} issuer definition: {err.messages}")
        raise err
    except Exception as err:
        LOGGER.error(f"Error handling {format} issuer webhook: {err}")
        raise err
