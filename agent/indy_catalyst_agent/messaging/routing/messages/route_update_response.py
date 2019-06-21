"""Response for a route update request."""

from typing import Sequence

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ..message_types import ROUTE_UPDATE_RESPONSE
from ..models.route_updated import RouteUpdated, RouteUpdatedSchema

HANDLER_CLASS = (
    "indy_catalyst_agent.messaging.routing.handlers"
    + ".route_update_response_handler.RouteUpdateResponseHandler"
)


class RouteUpdateResponse(AgentMessage):
    """Response for a route update request."""

    class Meta:
        """RouteUpdateResponse metadata."""

        handler_class = HANDLER_CLASS
        message_type = ROUTE_UPDATE_RESPONSE
        schema_class = "RouteUpdateResponseSchema"

    def __init__(self, *, updated: Sequence[RouteUpdated] = None, **kwargs):
        """
        Initialize a RouteUpdateResponse message instance.

        Args:
            updated: A list of route updates
        """

        super(RouteUpdateResponse, self).__init__(**kwargs)
        self.updated = updated or []


class RouteUpdateResponseSchema(AgentMessageSchema):
    """RouteUpdateResponse message schema used in serialization/deserialization."""

    class Meta:
        """RouteUpdateResponseSchema metadata."""

        model_class = RouteUpdateResponse

    updated = fields.List(fields.Nested(RouteUpdatedSchema()), required=True)
