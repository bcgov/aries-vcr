"""Admin routes for presentations."""

import json

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import fields, Schema

from .manager import PresentationManager
from .models.presentation_exchange import (
    PresentationExchange,
    PresentationExchangeSchema,
)

from ...holder.base import BaseHolder
from ...storage.error import StorageNotFoundError


class PresentationExchangeListSchema(Schema):
    """Result schema for a presentation exchange query."""

    results = fields.List(fields.Nested(PresentationExchangeSchema()))


class PresentationRequestRequestSchema(Schema):
    """Request schema for sending a proof request."""

    class RequestedAttribute(Schema):
        """RequestedAttribute model."""

        name = fields.Str(required=True)
        restrictions = fields.List(fields.Dict(), required=False)

    class RequestedPredicate(Schema):
        """RequestedPredicate model."""

        name = fields.Str(required=True)
        p_type = fields.Str(required=True)
        p_value = fields.Str(required=True)
        restrictions = fields.List(fields.Dict(), required=False)

    connection_id = fields.Str(required=True)
    name = fields.String(required=True)
    version = fields.String(required=True)
    requested_attributes = fields.Nested(RequestedAttribute, many=True)
    requested_predicates = fields.Nested(RequestedPredicate, many=True)


class SendPresentationRequestSchema(Schema):
    """Request schema for sending a presentation."""

    self_attested_attributes = fields.Dict(required=True)
    requested_attributes = fields.Dict(required=True)
    requested_predicates = fields.Dict(required=True)


@docs(tags=["presentation_exchange"], summary="Fetch all presentation exchange records")
@response_schema(PresentationExchangeListSchema(), 200)
async def presentation_exchange_list(request: web.BaseRequest):
    """
    Request handler for searching presentation exchange records.

    Args:
        request: aiohttp request object

    Returns:
        The presentation exchange list response

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
    records = await PresentationExchange.query(context, tag_filter)
    return web.json_response({"results": [record.serialize() for record in records]})


@docs(
    tags=["presentation_exchange"],
    summary="Fetch a single presentation exchange record",
)
@response_schema(PresentationExchangeSchema(), 200)
async def presentation_exchange_retrieve(request: web.BaseRequest):
    """
    Request handler for fetching a single presentation exchange record.

    Args:
        request: aiohttp request object

    Returns:
        The presentation exchange record response

    """
    context = request.app["request_context"]
    presentation_exchange_id = request.match_info["id"]
    try:
        record = await PresentationExchange.retrieve_by_id(
            context, presentation_exchange_id
        )
    except StorageNotFoundError:
        return web.HTTPNotFound()
    return web.json_response(record.serialize())


@docs(
    tags=["presentation_exchange"],
    parameters=[
        {
            "name": "start",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "count",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "extra_query",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
    ],
    summary="Fetch credentials for a presentation request from wallet",
)
# @response_schema(ConnectionListSchema(), 200)
async def presentation_exchange_credentials_list(request: web.BaseRequest):
    """
    Request handler for searching applicable credential records.

    Args:
        request: aiohttp request object

    Returns:
        The credential list response

    """
    context = request.app["request_context"]

    presentation_exchange_id = request.match_info["id"]
    presentation_referent = request.match_info["referent"]

    try:
        presentation_exchange_record = await PresentationExchange.retrieve_by_id(
            context, presentation_exchange_id
        )
    except StorageNotFoundError:
        return web.HTTPNotFound()

    start = request.query.get("start")
    count = request.query.get("count")

    # url encoded json extra_query
    encoded_extra_query = request.query.get("extra_query") or "{}"
    extra_query = json.loads(encoded_extra_query)

    # defaults
    start = int(start) if isinstance(start, str) else 0
    count = int(count) if isinstance(count, str) else 10

    holder: BaseHolder = await context.inject(BaseHolder)
    credentials = await holder.get_credentials_for_presentation_request_by_referent(
        presentation_exchange_record.presentation_request,
        presentation_referent,
        start,
        count,
        extra_query,
    )

    return web.json_response(credentials)


@docs(tags=["presentation_exchange"], summary="Sends a presentation request")
@request_schema(PresentationRequestRequestSchema())
async def presentation_exchange_send_request(request: web.BaseRequest):
    """
    Request handler for sending a presentation request.

    Args:
        request: aiohttp request object

    Returns:
        The presentation exchange details.

    """

    context = request.app["request_context"]
    outbound_handler = request.app["outbound_message_router"]

    body = await request.json()

    connection_id = body.get("connection_id")

    name = body.get("name")
    version = body.get("version")
    requested_attributes = body.get("requested_attributes")
    requested_predicates = body.get("requested_predicates")

    presentation_manager = PresentationManager(context)

    (
        presentation_exchange_record,
        presentation_request_message,
    ) = await presentation_manager.create_request(
        name, version, requested_attributes, requested_predicates, connection_id
    )

    await outbound_handler(presentation_request_message, connection_id=connection_id)

    return web.json_response(presentation_exchange_record.serialize())


@docs(tags=["presentation_exchange"], summary="Sends a credential presentation")
@request_schema(SendPresentationRequestSchema())
@response_schema(PresentationExchangeSchema())
async def presentation_exchange_send_credential_presentation(request: web.BaseRequest):
    """
    Request handler for sending a credential presentation.

    Args:
        request: aiohttp request object

    Returns:
        The presentation exchange details.

    """

    context = request.app["request_context"]
    outbound_handler = request.app["outbound_message_router"]
    presentation_exchange_id = request.match_info["id"]

    body = await request.json()

    presentation_exchange_record = await PresentationExchange.retrieve_by_id(
        context, presentation_exchange_id
    )
    connection_id = presentation_exchange_record.connection_id

    assert (
        presentation_exchange_record.state
        == presentation_exchange_record.STATE_REQUEST_RECEIVED
    )

    presentation_manager = PresentationManager(context)

    (
        presentation_exchange_record,
        presentation_message,
    ) = await presentation_manager.create_presentation(
        presentation_exchange_record, body
    )

    await outbound_handler(presentation_message, connection_id=connection_id)
    return web.json_response(presentation_exchange_record.serialize())


@docs(
    tags=["presentation_exchange"], summary="Verify a received credential presentation"
)
@response_schema(PresentationExchangeSchema())
async def presentation_exchange_verify_credential_presentation(
    request: web.BaseRequest
):
    """
    Request handler for verifying a presentation request.

    Args:
        request: aiohttp request object

    Returns:
        The presentation exchange details.

    """

    context = request.app["request_context"]
    presentation_exchange_id = request.match_info["id"]

    presentation_exchange_record = await PresentationExchange.retrieve_by_id(
        context, presentation_exchange_id
    )

    assert (
        presentation_exchange_record.state
        == presentation_exchange_record.STATE_PRESENTATION_RECEIVED
    )

    presentation_manager = PresentationManager(context)

    presentation_exchange_record = await presentation_manager.verify_presentation(
        presentation_exchange_record
    )

    return web.json_response(presentation_exchange_record.serialize())


@docs(
    tags=["presentation_exchange"],
    summary="Remove an existing presentation exchange record",
)
async def presentation_exchange_remove(request: web.BaseRequest):
    """
    Request handler for removing a presentation exchange record.

    Args:
        request: aiohttp request object
    """
    context = request.app["request_context"]
    presentation_exchange_id = request.match_info["id"]
    try:
        presentation_exchange_id = request.match_info["id"]
        presentation_exchange_record = await PresentationExchange.retrieve_by_id(
            context, presentation_exchange_id
        )
    except StorageNotFoundError:
        return web.HTTPNotFound()
    await presentation_exchange_record.delete_record(context)
    return web.HTTPOk()


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [
            web.get("/presentation_exchange", presentation_exchange_list),
            web.get("/presentation_exchange/{id}", presentation_exchange_retrieve),
            web.get(
                "/presentation_exchange/{id}/credentials/{referent}",
                presentation_exchange_credentials_list,
            ),
            web.post(
                "/presentation_exchange/send_request",
                presentation_exchange_send_request,
            ),
            web.post(
                "/presentation_exchange/{id}/send_presentation",
                presentation_exchange_send_credential_presentation,
            ),
            web.post(
                "/presentation_exchange/{id}/verify_presentation",
                presentation_exchange_verify_credential_presentation,
            ),
            web.post(
                "/presentation_exchange/{id}/remove", presentation_exchange_remove
            ),
        ]
    )
