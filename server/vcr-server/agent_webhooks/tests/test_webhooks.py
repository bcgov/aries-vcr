from unittest.mock import patch
from django.test import TestCase
from marshmallow import ValidationError

from agent_webhooks.utils.issuer import IssuerRegistrationResult
from agent_webhooks.views import TOPIC_VC_DI_ISSUER


class TestWebhooks(TestCase):

    BASE_URL = "agentcb/topic"

    @patch(
        "agent_webhooks.views.handle_vc_di_issuer",
        autospec=True,
        return_value=IssuerRegistrationResult(None, [], []),
    )
    def test_vc_di_issuer_topic(self, mock_handle_issuer, *_):
        f"""Test the {TOPIC_VC_DI_ISSUER} topic handler is called."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_ISSUER}/", {"message": "test"}
        )

        mock_handle_issuer.assert_called_once()
        assert response.status_code == 200

        response_data = response.json()

        assert "issuer" in response_data
        assert type(response_data["issuer"]) == dict
        assert "schemas" in response_data
        assert len(response_data["schemas"]) == 0
        assert "credential_types" in response_data
        assert len(response_data["credential_types"]) == 0

    def test_vc_di_issuer_topic_invalid_message(self, *_):
        f"""Test the {TOPIC_VC_DI_ISSUER} topic handler with an invalid message returns a validation error."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_ISSUER}/", {"invalid": "test"}
        )

        assert response.status_code == 422

    @patch(
        "agent_webhooks.views.handle_vc_di_issuer",
        autospec=True,
        side_effect=Exception("Test exception raised"),
    )
    def test_vc_di_issuer_topic_exception(self, *_):
        f"""Test the {TOPIC_VC_DI_ISSUER} topic handler returns an exception."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_ISSUER}/", {"message": "test"}
        )

        assert response.status_code == 500
