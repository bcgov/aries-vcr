"""Connection handling admin routes."""

import json

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import fields, Schema

from .manager import CredentialManager
from ..connections.manager import ConnectionManager
from ..connections.models.connection_record import ConnectionRecord


class CredentialOfferRequestSchema(Schema):
    """Result schema for a new connection invitation."""

    connection_id = fields.Str(required=True)
    credential_definition_id = fields.Str(required=True)


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
@request_schema(CredentialOfferRequestSchema())
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
    outbound_handler = request.app["outbound_message_router"]

    body = await request.json()

    connection_id = body.get("connection_id")
    credential_definition_id = body.get("credential_definition_id")

    connection_manager = ConnectionManager(context)
    credential_manager = CredentialManager(context)

    connection_record = await ConnectionRecord.retrieve_by_id(
        context.storage, connection_id
    )

    connection_target = await connection_manager.get_connection_target(
        connection_record
    )

    # TODO: validate connection_record valid

    credential_exchange_record, credential_offer_message = await credential_manager.create_offer(
        credential_definition_id
    )

    await outbound_handler(credential_offer_message, connection_target)

    return web.json_response(credential_exchange_record.serialize())


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

    # TODO: Once the entire credential flow is not automatic, we can allow
    #       manual triggering of sending a credential request
    #       (in response to an existing credential offer)
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
    # TODO: Once the entire credential flow is not automatic, we can allow
    #       manual triggering of issueing a credential
    pass


async def register(app: web.Application):
    """Register routes."""
    app.add_routes([web.post("/credentials/send-offer", credentials_send_offer)])
    app.add_routes(
        [web.post("/credentials/{id}/send-request", credentials_send_request)]
    )
    app.add_routes([web.post("/credentials/{id}/issue", credentials_issue)])
