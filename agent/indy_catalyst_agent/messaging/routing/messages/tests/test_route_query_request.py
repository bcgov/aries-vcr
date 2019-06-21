from ..route_query_request import RouteQueryRequest
from ...message_types import ROUTE_QUERY_REQUEST
from ...models.paginate import Paginate, PaginateSchema

from unittest import mock, TestCase


class TestRouteQueryRequest(TestCase):
    test_limit = 100
    test_offset = 10
    test_verkey = "3Dn1SJNPaCXcvvJvSbsFWP2xaCjMom3can8CQNhWrTRx"
    test_filter = {"recipient_key": "3Dn1SJNPaCXcvvJvSbsFWP2xaCjMom3can8CQNhWrTRx"}

    def setUp(self):
        self.paginate = Paginate(limit=self.test_limit, offset=self.test_offset)
        self.message = RouteQueryRequest(
            filter=self.test_filter, paginate=self.paginate
        )

    def test_init(self):
        assert self.message.filter == self.test_filter
        assert self.message.paginate.limit == self.test_limit
        assert self.message.paginate.offset == self.test_offset

    def test_type(self):
        assert self.message._type == ROUTE_QUERY_REQUEST

    @mock.patch(
        "indy_catalyst_agent.messaging.routing.messages.route_query_request.RouteQueryRequestSchema.load"
    )
    def test_deserialize(self, message_schema_load):
        obj = {"obj": "obj"}

        message = RouteQueryRequest.deserialize(obj)
        message_schema_load.assert_called_once_with(obj)

        assert message is message_schema_load.return_value

    @mock.patch(
        "indy_catalyst_agent.messaging.routing.messages.route_query_request.RouteQueryRequestSchema.dump"
    )
    def test_serialize(self, message_schema_dump):
        message_dict = self.message.serialize()
        message_schema_dump.assert_called_once_with(self.message)

        assert message_dict is message_schema_dump.return_value


class TestRouteQueryRequestSchema(TestCase):
    def test_make_model(self):
        message = RouteQueryRequest(filter={}, paginate=Paginate())
        data = message.serialize()
        model_instance = RouteQueryRequest.deserialize(data)
        assert isinstance(model_instance, RouteQueryRequest)
