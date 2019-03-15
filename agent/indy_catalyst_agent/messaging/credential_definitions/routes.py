"""Connection handling admin routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from marshmallow import fields, Schema


class CredentialDefinitionSendRequestSchema(Schema):
    """Request schema for schema send request."""

    schema_id = fields.Str()


class CredentialDefinitionSendResultsSchema(Schema):
    """Results schema for schema send request."""

    credential_definition_id = fields.Str()


class CredentialDefinitionGetResultsSchema(Schema):
    """Results schema for schema get request."""

    credential_definition = fields.Dict()


@docs(
    tags=["credential-definition"],
    summary="Sends a credential definition to the ledger",
)
@request_schema(CredentialDefinitionSendRequestSchema())
@response_schema(CredentialDefinitionSendResultsSchema(), 200)
async def credential_definitions_send_credential_definition(request: web.BaseRequest):
    """
    Request handler for sending a credential definition to the ledger.

    Args:
        request: aiohttp request object

    Returns:
        The credential offer details.

    """

    context = request.app["request_context"]

    body = await request.json()

    schema_id = body.get("schema_id")

    async with context.ledger:
        credential_definition_id = await context.ledger.send_credential_definition(
            schema_id
        )

    return web.json_response({"credential_definition_id": credential_definition_id})


@docs(
    tags=["credential-definition"],
    summary="Gets a credential definition from the ledger",
)
@response_schema(CredentialDefinitionGetResultsSchema(), 200)
async def credential_definitions_get_credential_definition(request: web.BaseRequest):
    """
    Request handler for getting a credential definition from the ledger.

    Args:
        request: aiohttp request object

    Returns:
        The credential offer details.

    """

    context = request.app["request_context"]

    credential_definition_id = request.match_info["id"]

    async with context.ledger:
        credential_definition = await context.ledger.get_credential_definition(
            credential_definition_id
        )

    return web.json_response({"credential_definition": credential_definition})


async def register(app: web.Application):
    """Register routes."""
    app.add_routes(
        [
            web.post(
                "/credential-definitions",
                credential_definitions_send_credential_definition,
            )
        ]
    )
    app.add_routes(
        [
            web.get(
                "/credential-definitions/{id}",
                credential_definitions_get_credential_definition,
            )
        ]
    )
