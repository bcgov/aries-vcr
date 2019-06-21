from ..disclose import Disclose
from ...message_types import DISCLOSE

from unittest import mock, TestCase


class TestDisclose(TestCase):
    test_protocols = [
        {
            "pid": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message",
            "roles": [],
        }
    ]

    def test_init(self):
        disclose = Disclose(protocols=self.test_protocols)
        assert disclose.protocols == self.test_protocols

    def test_type(self):
        disclose = Disclose(protocols=self.test_protocols)
        assert disclose._type == DISCLOSE

    @mock.patch(
        "indy_catalyst_agent.messaging.discovery.messages.disclose.DiscloseSchema.load"
    )
    def test_deserialize(self, mock_disclose_schema_load):
        obj = {"obj": "obj"}

        disclose = Disclose.deserialize(obj)
        mock_disclose_schema_load.assert_called_once_with(obj)

        assert disclose is mock_disclose_schema_load.return_value

    @mock.patch(
        "indy_catalyst_agent.messaging.discovery.messages.disclose.DiscloseSchema.dump"
    )
    def test_serialize(self, mock_disclose_schema_dump):
        disclose = Disclose(protocols=self.test_protocols)

        disclose_dict = disclose.serialize()
        mock_disclose_schema_dump.assert_called_once_with(disclose)

        assert disclose_dict is mock_disclose_schema_dump.return_value


class TestDiscloseSchema(TestCase):

    disclose = Disclose(protocols=[])

    def test_make_model(self):
        data = self.disclose.serialize()
        model_instance = Disclose.deserialize(data)
        assert isinstance(model_instance, Disclose)
