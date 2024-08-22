import json

from unittest.mock import patch
from django.test import TestCase
from marshmallow import ValidationError

from agent_webhooks.handlers.vc_di_credential_type import handle_credential_type
from agent_webhooks.tests.data import issuer_def_spec, credential_type_def_spec


class TestIssuerHandler(TestCase):
    """
    Tests for the credential type webhook message handler.

    Note: saving to JSONField is not supported when we use sqlite as the back-end (in testing)
    """

    # We need to convert the processor config to None for testing because it is a JSONField
    @patch(
        "agent_webhooks.utils.credential_type.CredentialTypeManager._build_processor_config",
        return_value=None,
    )
    def test_handle_credential_type(self, *_):
        """Test the handle_credential type function."""

        test_message = {
            "issuer": issuer_def_spec.copy(),
            "credential_type": credential_type_def_spec.copy(),
        }

        result = handle_credential_type(test_message)

        assert result.issuer is not None
        issuer = result.issuer

        assert issuer.name == issuer_def_spec.get("name")
        assert issuer.did == issuer_def_spec.get("did")
        assert issuer.abbreviation == issuer_def_spec.get("abbreviation")
        assert issuer.email == issuer_def_spec.get("email")
        assert issuer.url == issuer_def_spec.get("url")
        assert issuer.endpoint == issuer_def_spec.get("endpoint")
        assert issuer.logo_b64 == issuer_def_spec.get("logo_b64")

        assert result.schemas is not None
        assert len(result.schemas) == 1

        schema = result.schemas[0]
        assert schema.name == credential_type_def_spec.get("schema")
        assert schema.version == credential_type_def_spec.get("version")
        assert schema.origin_did == issuer_def_spec.get("did")

        assert result.credential_types is not None
        assert len(result.credential_types) == 1

        credential_type = result.credential_types[0]
        assert credential_type.issuer_id == issuer.id
        assert credential_type.schema_id == schema.id

    def test_handle_credential_type_invalid_message(self):
        """
        Test the handle_credential_type function with an invalid message raises a validation error.
        """

        test_message = {
            "issuer_registration": {
                "issuer": issuer_def_spec.copy(),
                "credential_type": credential_type_def_spec.copy(),
            }
        }

        with self.assertRaises(ValidationError) as exc_info:
            handle_credential_type(test_message)

        assert "issuer_registration" in str(exc_info.exception)

    def test_handle_credential_type_invalid_message_missing_credential_type(self):
        """
        Test the handle_credential_type function with an invalid message raises a validation error:
        missing credential_type.
        """

        test_message = {
            "issuer": issuer_def_spec.copy(),
        }

        with self.assertRaises(ValidationError) as exc_info:
            handle_credential_type(test_message)

        assert "credential_type" in str(exc_info.exception)

    @patch(
        "agent_webhooks.handlers.vc_di_credential_type.handle_credential_type",
        side_effect=Exception("Test exception raised"),
    )
    def test_handle_credential_type_exception(self, mock_handle_credential_type):
        """Test the handle_credential_type function raises an exception."""

        test_message = {
            "issuer": issuer_def_spec.copy(),
            "credential_type": credential_type_def_spec.copy(),
        }

        with self.assertRaises(Exception) as exc_info:
            mock_handle_credential_type(test_message)

        assert "Test exception raised" in str(exc_info.exception)
