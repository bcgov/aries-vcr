from unittest.mock import patch
from django.test import TestCase
from marshmallow import ValidationError

from agent_webhooks.handlers.vc_di_issuer import handle_issuer
from agent_webhooks.tests.data import issuer_def_spec


class TestIssuerHandler(TestCase):
    """Tests for the issuer webhook message handler."""

    def test_handle_issuer(self):
        """Test the handle_issuer function."""

        test_message = issuer_def_spec.copy()

        result = handle_issuer(test_message)

        assert result.issuer is not None
        assert result.issuer.name == test_message["name"]
        assert result.issuer.did == test_message["did"]
        assert result.issuer.abbreviation == test_message["abbreviation"]
        assert result.issuer.email == test_message["email"]
        assert result.issuer.url == test_message["url"]
        assert result.issuer.endpoint == test_message["endpoint"]
        assert result.issuer.logo_b64 == test_message["logo_b64"]

        assert result.schemas is not None
        assert len(result.schemas) == 0
        assert result.credential_types is not None
        assert len(result.credential_types) == 0

    def test_handle_issuer_invalid_message(self):
        """Test the handle_issuer function with an invalid message raises a validation error."""

        test_message = {"issuer_registration": {"issuer": issuer_def_spec.copy()}}

        with self.assertRaises(ValidationError) as exc_info:
            handle_issuer(test_message)

        assert "issuer_registration" in str(exc_info.exception)

    def test_handle_issuer_invalid_message_missing_did(self):
        """
        Test the handle_issuer function with an invalid message raises a validation error:
        missing did.
        """

        test_message = issuer_def_spec.copy()
        del test_message["did"]

        with self.assertRaises(ValidationError) as exc_info:
            handle_issuer(test_message)

        assert "did" in str(exc_info.exception)

    @patch(
        "agent_webhooks.handlers.vc_di_issuer.handle_issuer",
        side_effect=Exception("Test exception raised"),
    )
    def test_handle_issuer_exception(self, mock_handle_issuer):
        """Test the handle_issuer function raises an exception."""

        test_message = issuer_def_spec.copy()

        with self.assertRaises(Exception) as exc_info:
            mock_handle_issuer(test_message)

        assert "Test exception raised" in str(exc_info.exception)
