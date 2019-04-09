from unittest import mock, TestCase

from asynctest import TestCase as AsyncTestCase

from ..ping_response import PingResponse
from ...message_types import PING_RESPONSE


class TestPingResponse(TestCase):
    def setUp(self):
        self.test_comment = "hello"

        self.test_ping = PingResponse(comment=self.test_comment)

    def test_init(self):
        """Test initialization."""
        assert self.test_ping.comment == self.test_comment

    def test_type(self):
        """Test type."""
        assert self.test_ping._type == PING_RESPONSE

    @mock.patch(
        "indy_catalyst_agent.messaging.trustping.messages.ping_response.PingResponseSchema.load"
    )
    def test_deserialize(self, mock_ping_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        msg = PingResponse.deserialize(obj)
        mock_ping_schema_load.assert_called_once_with(obj)

        assert msg is mock_ping_schema_load.return_value

    @mock.patch(
        "indy_catalyst_agent.messaging.trustping.messages.ping_response.PingResponseSchema.dump"
    )
    def test_serialize(self, mock_ping_schema_load):
        """
        Test serialization.
        """
        msg_dict = self.test_ping.serialize()
        mock_ping_schema_load.assert_called_once_with(self.test_ping)

        assert msg_dict is mock_ping_schema_load.return_value


class TestPingResponseSchema(AsyncTestCase):
    """Test ping response schema."""

    async def test_make_model(self):
        ping = PingResponse(comment="hello")
        data = ping.serialize()
        model_instance = PingResponse.deserialize(data)
        assert type(model_instance) is type(ping)
