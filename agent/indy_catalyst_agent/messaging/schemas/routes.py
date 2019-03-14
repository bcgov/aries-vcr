"""Connection handling admin routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from marshmallow import fields, Schema


class SchemaRequestSchema(Schema):
    """Result schema for a new connection invitation."""

    schema_name = fields.Str(required=True)
    schema_version = fields.Str(required=True)
    attributes = fields.List(fields.Str(), required=True)


class SchemaResultsSchema(Schema):
    """Result schema for a new connection invitation."""

    schema_id = fields.Int()
    schema_json = fields.Str()


@docs(tags=["schema"], summary="Sends a schema to the ledger")
@request_schema(SchemaRequestSchema())
@response_schema(SchemaResultsSchema(), 200)
async def schemas_send_schema(request: web.BaseRequest):
    """
    Request handler for sending a credential offer.

    Args:
        request: aiohttp request object

    Returns:
        The credential offer details.

    """

    context = request.app["request_context"]

    body = await request.json()

    schema_name = body.get("schema_name")
    schema_version = body.get("schema_version")
    attributes = body.get("attributes")

    async with context.ledger:
        schema_id = await context.ledger.send_schema(
            schema_name, schema_version, attributes
        )

    return web.json_response({"schema_id": schema_id})


@docs(tags=["schema"], summary="Gets a schema from the ledger")
@response_schema(SchemaResultsSchema(), 200)
async def schemas_get_schema(request: web.BaseRequest):
    """
    Request handler for sending a credential offer.

    Args:
        request: aiohttp request object

    Returns:
        The credential offer details.

    """

    context = request.app["request_context"]

    schema_id = request.match_info["id"]

    async with context.ledger:
        schema = await context.ledger.get_schema(schema_id)

    return web.json_response({"schema_id": schema_id, "schema_json": schema})


async def register(app: web.Application):
    """Register routes."""
    app.add_routes([web.post("/schemas", schemas_send_schema)])
    app.add_routes([web.get("/schemas/{id}", schemas_get_schema)])
