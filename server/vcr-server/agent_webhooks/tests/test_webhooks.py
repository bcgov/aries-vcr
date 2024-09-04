from unittest.mock import patch
from django.test import TestCase

from agent_webhooks.tests.data import credential_type_def_spec, issuer_def_spec
from agent_webhooks.utils.issuer import IssuerRegistrationResult
from agent_webhooks.views import TOPIC_VC_DI_CREDENTIAL_TYPE, TOPIC_VC_DI_ISSUER


class TestWebhooks(TestCase):
    """
    Tests for webhooks.

    Note: saving to JSONField is not supported when we use sqlite as the back-end (in testing)
    """

    BASE_URL = "agentcb/topic"

    @patch(
        "agent_webhooks.views.handle_vc_di_issuer",
        return_value=IssuerRegistrationResult(None, [], []),
    )
    def test_vc_di_issuer_topic(self, mock_handle_issuer):
        f"""Test the {TOPIC_VC_DI_ISSUER} topic handler is called."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_ISSUER}/",
            data={"message": "test"},
            content_type="application/json",
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

    def test_vc_di_issuer_topic_valid_message(self):
        f"""Test the {TOPIC_VC_DI_ISSUER} topic handler with a valid message."""

        test_message = issuer_def_spec.copy()

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_ISSUER}/",
            data=test_message,
            content_type="application/json",
        )

        assert response.status_code == 200

        response_data = response.json()

        assert "issuer" in response_data
        assert type(response_data["issuer"]) == dict
        assert "schemas" in response_data
        assert len(response_data["schemas"]) == 0
        assert "credential_types" in response_data
        assert len(response_data["credential_types"]) == 0

    def test_vc_di_issuer_topic_invalid_message(self):
        f"""Test the {TOPIC_VC_DI_ISSUER} topic handler with an invalid message returns a validation error."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_ISSUER}/",
            data={"invalid": "test"},
            content_type="application/json",
        )

        assert response.status_code == 422

    @patch(
        "agent_webhooks.views.handle_vc_di_issuer",
        side_effect=Exception("Test exception raised"),
    )
    def test_vc_di_issuer_topic_exception(self, *_):
        f"""Test the {TOPIC_VC_DI_ISSUER} topic handler returns an exception."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_ISSUER}/",
            data={"message": "test"},
            content_type="application/json",
        )

        assert response.status_code == 500

    @patch(
        "agent_webhooks.views.handle_vc_di_credential_type",
        return_value=IssuerRegistrationResult(None, [], []),
    )
    def test_vc_di_credential_type_topic(self, mock_handle_credential_type):
        f"""Test the {TOPIC_VC_DI_CREDENTIAL_TYPE} topic handler is called."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_CREDENTIAL_TYPE}/",
            data={"message": "test"},
            content_type="application/json",
        )

        mock_handle_credential_type.assert_called_once()
        assert response.status_code == 200

        response_data = response.json()

        assert "issuer" in response_data
        assert type(response_data["issuer"]) == dict
        assert "schemas" in response_data
        assert len(response_data["schemas"]) == 0
        assert "credential_types" in response_data
        assert len(response_data["credential_types"]) == 0

    # We need to convert the processor config to None for testing because it is a JSONField
    @patch(
        "agent_webhooks.utils.credential_type.CredentialTypeManager._build_processor_config",
        return_value=None,
    )
    def test_vc_di_credential_type_topic_valid_message(self, *_):
        f"""Test the {TOPIC_VC_DI_CREDENTIAL_TYPE} topic handler with a valid message."""

        test_message = {
            "issuer": issuer_def_spec.copy(),
            "credential_type": credential_type_def_spec.copy(),
        }

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_CREDENTIAL_TYPE}/",
            data=test_message,
            content_type="application/json",
        )

        assert response.status_code == 200

        response_data = response.json()

        assert "issuer" in response_data
        assert type(response_data["issuer"]) == dict
        assert "schemas" in response_data
        assert len(response_data["schemas"]) == 1
        assert "credential_types" in response_data
        assert len(response_data["credential_types"]) == 1

    def test_vc_di_credential_type_topic_invalid_message(self):
        f"""Test the {TOPIC_VC_DI_CREDENTIAL_TYPE} topic handler with an invalid message returns a validation error."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_CREDENTIAL_TYPE}/",
            data={"invalid": "test"},
            content_type="application/json",
        )

        assert response.status_code == 422

    @patch(
        "agent_webhooks.views.handle_vc_di_credential_type",
        side_effect=Exception("Test exception raised"),
    )
    def test_vc_di_credential_type_topic_exception(self, *_):
        f"""Test the {TOPIC_VC_DI_CREDENTIAL_TYPE} topic handler returns an exception."""

        response = self.client.post(
            f"/{self.BASE_URL}/{TOPIC_VC_DI_CREDENTIAL_TYPE}/",
            data={"message": "test"},
            content_type="application/json",
        )

        assert response.status_code == 500
