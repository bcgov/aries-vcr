import logging

from marshmallow import ValidationError

from api.v2.models.Credential import Credential
from api.v4.serializers.rest.credential import CredentialSerializer

from agent_webhooks.enums import FormatEnum
from agent_webhooks.schemas import CredentialDefSchema
from agent_webhooks.utils.vc_di_credential import CredentialManager

LOGGER = logging.getLogger(__name__)

format = FormatEnum.VC_DI.value

def handle_credential(
    message: CredentialDefSchema,
) -> Credential:
    f"""Webhook message handler for a {format} credential."""

    try:
        credential_schema = CredentialDefSchema()
        credential_schema.load(message)
        credential_manager = CredentialManager()

        credential = credential_manager.update_credential(message)
        return CredentialSerializer(credential).data
    except ValidationError as err:
        LOGGER.error(f"Invalid {format} credential type definition: {err.messages}")
        raise err
    except Exception as err:
        LOGGER.error(f"Error handling {format} credential type webhook: {err}")
        raise err