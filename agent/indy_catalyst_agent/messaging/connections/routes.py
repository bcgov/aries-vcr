"""Connection handling admin routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from marshmallow import fields, Schema

from .manager import ConnectionManager
from .messages.connection_invitation import (
    ConnectionInvitation,
    ConnectionInvitationSchema,
)
from .models.connection_record import ConnectionRecord, ConnectionRecordSchema
from ...storage.error import StorageNotFoundError


class ConnectionListSchema(Schema):
    """Result schema for connection list."""

    results = fields.List(fields.Nested(ConnectionRecordSchema()))


class InvitationResultSchema(Schema):
    """Result schema for a new connection invitation."""

    connection_id = fields.Str()
    invitation = fields.Nested(ConnectionInvitationSchema())
    invitation_url = fields.Str()


def connection_sort_key(conn):
    """Get the sorting key for a particular connection."""
    if conn["state"] == ConnectionRecord.STATE_INACTIVE:
        pfx = "2"
    elif conn["state"] == ConnectionRecord.STATE_INVITATION:
        pfx = "1"
    else:
        pfx = "0"
    return pfx + conn["created_at"]


@docs(
    tags=["connection"],
    summary="Query agent-to-agent connections",
    parameters=[
        {
            "name": "initiator",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "invitation_key",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "my_did",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "state",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "their_did",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "their_role",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
    ],
)
@response_schema(ConnectionListSchema(), 200)
async def connections_list(request: web.BaseRequest):
    """
    Request handler for searching connection records.

    Args:
        request: aiohttp request object

    Returns:
        The connection list response

    """
    context = request.app["request_context"]
    tag_filter = {}
    for param_name in (
        "initiator",
        "invitation_id",
        "my_did",
        "state",
        "their_did",
        "their_role",
    ):
        if param_name in request.query and request.query[param_name] != "":
            tag_filter[param_name] = request.query[param_name]
    records = await ConnectionRecord.query(context, tag_filter)
    results = []
    for record in records:
        row = record.serialize()
        row["activity"] = await record.fetch_activity(context)
        results.append(row)
    results.sort(key=connection_sort_key)
    return web.json_response({"results": results})


@docs(tags=["connection"], summary="Fetch a single connection record")
@response_schema(ConnectionRecordSchema(), 200)
async def connections_retrieve(request: web.BaseRequest):
    """
    Request handler for fetching a single connection record.

    Args:
        request: aiohttp request object

    Returns:
        The connection record response

    """
    context = request.app["request_context"]
    connection_id = request.match_info["id"]
    try:
        record = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        return web.HTTPNotFound()
    return web.json_response(record.serialize())


@docs(tags=["connection"], summary="Create a new connection invitation")
@response_schema(InvitationResultSchema(), 200)
async def connections_create_invitation(request: web.BaseRequest):
    """
    Request handler for creating a new connection invitation.

    Args:
        request: aiohttp request object

    Returns:
        The connection invitation details

    """
    context = request.app["request_context"]
    connection_mgr = ConnectionManager(context)
    connection, invitation = await connection_mgr.create_invitation()
    result = {
        "connection_id": connection.connection_id,
        "invitation": invitation.serialize(),
        "invitation_url": invitation.to_url(),
    }
    return web.json_response(result)


@docs(tags=["connection"], summary="Receive a new connection invitation")
@request_schema(ConnectionInvitationSchema())
@response_schema(ConnectionRecordSchema(), 200)
async def connections_receive_invitation(request: web.BaseRequest):
    """
    Request handler for receiving a new connection invitation.

    Args:
        request: aiohttp request object

    Returns:
        The resulting connection record details

    """
    context = request.app["request_context"]
    if context.settings.get("admin.no_receive_invites"):
        return web.HTTPForbidden()
    connection_mgr = ConnectionManager(context)
    outbound_handler = request.app["outbound_message_router"]
    invitation_json = await request.json()
    invitation = ConnectionInvitation.deserialize(invitation_json)
    connection = await connection_mgr.receive_invitation(invitation)
    if context.settings.get("accept_invites"):
        request = await connection_mgr.create_request(connection)
        await outbound_handler(request, connection_id=connection.connection_id)
    return web.json_response(connection.serialize())


@docs(
    tags=["connection"],
    summary="Accept a stored connection invitation",
    parameters=[
        {
            "name": "my_endpoint",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
        {
            "name": "my_label",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        },
    ],
)
@response_schema(ConnectionRecordSchema(), 200)
async def connections_accept_invitation(request: web.BaseRequest):
    """
    Request handler for accepting a stored connection invitation.

    Args:
        request: aiohttp request object

    Returns:
        The resulting connection record details

    """
    context = request.app["request_context"]
    outbound_handler = request.app["outbound_message_router"]
    connection_id = request.match_info["id"]
    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        return web.HTTPNotFound()
    connection_mgr = ConnectionManager(context)
    my_label = request.query.get("my_label") or None
    my_endpoint = request.query.get("my_endpoint") or None
    request = await connection_mgr.create_request(connection, my_label, my_endpoint)
    await outbound_handler(request, connection_id=connection.connection_id)
    return web.json_response(connection.serialize())


@docs(
    tags=["connection"],
    summary="Accept a stored connection request",
    parameters=[
        {
            "name": "my_endpoint",
            "in": "query",
            "schema": {"type": "string"},
            "required": False,
        }
    ],
)
@response_schema(ConnectionRecordSchema(), 200)
async def connections_accept_request(request: web.BaseRequest):
    """
    Request handler for accepting a stored connection request.

    Args:
        request: aiohttp request object

    Returns:
        The resulting connection record details

    """
    context = request.app["request_context"]
    outbound_handler = request.app["outbound_message_router"]
    connection_id = request.match_info["id"]
    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        return web.HTTPNotFound()
    connection_mgr = ConnectionManager(context)
    my_endpoint = request.query.get("my_endpoint") or None
    request = await connection_mgr.create_response(connection, my_endpoint)
    await outbound_handler(request, connection_id=connection.connection_id)
    return web.json_response(connection.serialize())


@docs(
    tags=["connection"], summary="Assign another connection as the inbound connection"
)
async def connections_establish_inbound(request: web.BaseRequest):
    """
    Request handler for setting the inbound connection on a connection record.

    Args:
        request: aiohttp request object
    """
    context = request.app["request_context"]
    connection_id = request.match_info["id"]
    outbound_handler = request.app["outbound_message_router"]
    inbound_connection_id = request.match_info["ref_id"]
    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        return web.HTTPNotFound()
    connection_mgr = ConnectionManager(context)
    await connection_mgr.establish_inbound(
        connection, inbound_connection_id, outbound_handler
    )
    return web.HTTPOk()


@docs(tags=["connection"], summary="Remove an existing connection record")
async def connections_remove(request: web.BaseRequest):
    """
    Request handler for removing a connection record.

    Args:
        request: aiohttp request object
    """
    context = request.app["request_context"]
    connection_id = request.match_info["id"]
    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        return web.HTTPNotFound()
    await connection.delete_record(context)
    return web.HTTPOk()


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [
            web.get("/connections", connections_list),
            web.get("/connections/{id}", connections_retrieve),
            web.post("/connections/create-invitation", connections_create_invitation),
            web.post("/connections/receive-invitation", connections_receive_invitation),
            web.post(
                "/connections/{id}/accept-invitation", connections_accept_invitation
            ),
            web.post("/connections/{id}/accept-request", connections_accept_request),
            web.post(
                "/connections/{id}/establish-inbound/{ref_id}",
                connections_establish_inbound,
            ),
            web.post("/connections/{id}/remove", connections_remove),
        ]
    )
