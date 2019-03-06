"""Connection handling admin routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from marshmallow import fields, Schema

from .manager import CredentialManager

from ..connections.models.connection_record import ConnectionRecord
# from ..connections.manager import ConnectionManager

# from .messages.connection_invitation import (
#     ConnectionInvitation,
#     ConnectionInvitationSchema,
# )
# from .models.connection_record import ConnectionRecord, ConnectionRecordSchema
# from ...storage.error import StorageNotFoundError


class CredentialOfferResultSchema(Schema):
    """Result schema for a new connection invitation."""

    credential_id = fields.Str()


class CredentialRequestResultSchema(Schema):
    """Result schema for a new connection invitation."""

    credential_id = fields.Str()


class CredentialIssueResultSchema(Schema):
    """Result schema for a new connection invitation."""

    credential_id = fields.Str()


@docs(tags=["credential"], summary="Sends a credential offer")
@response_schema(CredentialOfferResultSchema(), 200)
async def credentials_send_offer(request: web.BaseRequest):
    """
    Request handler for sending a credential offer.

    Args:
        request: aiohttp request object

    Returns:
        The credential offer details.

    """

    context = request.app["request_context"]

    body = await request.json()
    credential_definition_id = body.get("credential_definition_id")
    connection_id = body.get("connection_id")

    credential_manager = CredentialManager(context)
    connection_record = await ConnectionRecord.retrieve_by_id(
        context.storage, connection_id
    )

    credential_offer = await credential_manager.send_credential_offer(
        connection_record, credential_definition_id
    )

    result = {"credential_offer": credential_offer}
    return web.json_response(result)


@docs(tags=["credential"], summary="Sends a credential request")
@response_schema(CredentialRequestResultSchema(), 200)
async def credentials_send_request(request: web.BaseRequest):
    """
    Request handler for sending a credential request.

    Args:
        request: aiohttp request object

    Returns:
        The credential request details.

    """
    pass


@docs(tags=["credential"], summary="Sends a credential")
@response_schema(CredentialIssueResultSchema(), 200)
async def credentials_issue(request: web.BaseRequest):
    """
    Request handler for sending a credential.

    Args:
        request: aiohttp request object

    Returns:
        The credential details.

    """
    pass


async def register(app: web.Application):
    """Register routes."""
    app.add_routes([web.post("/credentials/send-offer", credentials_send_offer)])
    app.add_routes(
        [web.post("/credentials/{id}/send-request", credentials_send_request)]
    )
    app.add_routes([web.post("/credentials/{id}/issue", credentials_issue)])
