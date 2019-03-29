from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from .models.presentation_exchange import PresentationExchange

from ...storage.error import StorageNotFoundError


@docs(tags=["presentation_exchange"], summary="Fetch all presentation exchange records")
# @response_schema(ConnectionListSchema(), 200)
async def presentation_exchange_list(request: web.BaseRequest):
    """
    Request handler for searching presentation exchange records.

    Args:
        request: aiohttp request object

    Returns:
        The connection list response

    """
    context = request.app["request_context"]
    tag_filter = {}
    for param_name in (
        "connection_id",
        "initiator",
        "state",
        "credential_definition_id",
        "schema_id",
    ):
        if param_name in request.query and request.query[param_name] != "":
            tag_filter[param_name] = request.query[param_name]
    records = await PresentationExchange.query(context.storage, tag_filter)
    return web.json_response({"results": [record.serialize() for record in records]})


@docs(
    tags=["presentation_exchange"],
    summary="Fetch a single presentation exchange record",
)
# @response_schema(ConnectionRecordSchema(), 200)
async def presentation_exchange_retrieve(request: web.BaseRequest):
    """
    Request handler for fetching a single connection record.

    Args:
        request: aiohttp request object

    Returns:
        The connection record response

    """
    context = request.app["request_context"]
    presentation_exchange_id = request.match_info["id"]
    try:
        record = await PresentationExchange.retrieve_by_id(
            context.storage, presentation_exchange_id
        )
    except StorageNotFoundError:
        return web.HTTPNotFound()
    return web.json_response(record.serialize())


async def register(app: web.Application):
    """Register routes."""

    app.add_routes([web.get("/presentation_exchange", presentation_exchange_list)])
    app.add_routes(
        [web.get("/presentation_exchange/{id}", presentation_exchange_retrieve)]
    )
