"""
Represents a connection request message.
"""

from marshmallow import Schema, fields, post_load

from ..agent_message import AgentMessage
from ..message_types import MessageTypes
from ..validators import must_not_be_blank

from ...models.agent_endpoint import AgentEndpoint, AgentEndpointSchema


class ConnectionRequest(AgentMessage):
    def __init__(self, endpoint: AgentEndpoint, did: str, verkey: str):
        self.endpoint = endpoint
        self.did = did
        self.verkey = verkey

    def _type(self):
        # Avoid clobbering builtin property
        return MessageTypes.CONNECTION_REQUEST.value


class ConnectionRequestSchema(Schema):
    # Avoid clobbering builtin property
    _type = fields.Str(data_key="@type", required=True)
    endpoint = fields.Nested(
        AgentEndpointSchema, validate=must_not_be_blank, required=True
    )
    did = fields.Str(required=True)
    verkey = fields.Str(required=True)

    @post_load
    def make_model(self, data: dict) -> ConnectionRequest:
        del data["_type"]
        return ConnectionRequest(**data)
