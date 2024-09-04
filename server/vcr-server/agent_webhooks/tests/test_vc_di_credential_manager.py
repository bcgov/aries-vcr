from datetime import datetime, timezone
from django.test import TestCase

from unittest.mock import MagicMock, patch

from api.v2.models import CredentialType, Issuer, Schema, Topic

from agent_webhooks.enums import FormatEnum
from agent_webhooks.utils.credential_type import CredentialTypeManager
from agent_webhooks.utils.vc_di_credential import CredentialManager, CredentialException

from agent_webhooks.tests.data import (
    credential_def_spec,
    credential_type_def_spec,
    issuer_def_spec,
)

format = FormatEnum.VC_DI.value


class TestCredentialManager(TestCase):
    f"""Tests for the {format} credential manager class."""

    def setUp(self):
        """Create an Issuer, Schema and CredentialType to test with"""

        self.issuer = Issuer.objects.create(**issuer_def_spec.copy())
        self.issuer.save()

        schema_def_spec = {
            "name": credential_type_def_spec.get("schema"),
            "version": credential_type_def_spec.get("version"),
            "origin_did": issuer_def_spec.get("did"),
        }
        self.schema = Schema.objects.create(**schema_def_spec)
        self.schema.save()

        self.processor_config = CredentialTypeManager()._build_processor_config(
            credential_type_def_spec.copy()
        )
        self.credential_type = CredentialType.objects.create(
            issuer=self.issuer, schema=self.schema
        )
        self.credential_type.save()

    def test_resolve_credential_type(self):
        """
        Test the _resolve_credential_type function returns a credential type.
        """

        mgr = CredentialManager()
        credential_type = mgr._resolve_credential_type(credential_def_spec.copy())

        assert credential_type is not None
        assert credential_type.issuer == self.issuer
        assert credential_type.schema == self.schema

    @patch("api.v2.models.Schema.objects.get", side_effect=Schema.DoesNotExist)
    def test_resolve_credential_type_schema_not_found(self, *_):
        """
        Test the _resolve_credential_type function raises an error:
        schema not found.
        """

        mgr = CredentialManager()

        with self.assertRaises(CredentialException) as exc_info:
            mgr._resolve_credential_type(credential_def_spec.copy())

        assert (
            "Schema with"
            + f" origin_did '{self.schema.origin_did}',"
            + f" name '{self.schema.name}',"
            + f" and version '{self.schema.version}'"
            + " does not exist."
            in str(exc_info.exception)
        )
        assert self.issuer is not None

    @patch("api.v2.models.Issuer.objects.get", side_effect=Issuer.DoesNotExist)
    def test_resolve_credential_type_issuer_not_found(self, *_):
        """
        Test the _resolve_credential_type function raises an error:
        issuer not found.
        """

        mgr = CredentialManager()

        with self.assertRaises(CredentialException) as exc_info:
            mgr._resolve_credential_type(credential_def_spec.copy())

        assert "Issuer with" + f" did '{self.issuer.did}' " + "does not exist." in str(
            exc_info.exception
        )
        assert self.schema is not None

    @patch("api.v2.models.Topic.objects.get", autospec=True)
    def test_resolve_credential_topic(self, mock_topic_get):
        """Test the _resolve_credential_topic function returns a topic."""

        mock_topic_get.return_value = Topic(
            source_id="A0131571", type="registration.registries.ca"
        )

        mgr = CredentialManager()

        topic = mgr._resolve_credential_topic(
            credential_def_spec.copy(), self.processor_config
        )

        assert topic is not None

    @patch(
        "agent_webhooks.utils.vc_di_credential.CredentialManager._process_mapping",
        return_value=None,
    )
    def test_resolve_credential_topic_from_processor_config_not_found(self, *_):
        """
        Test the _resolve_credential_topic function raises an error:
        source id or type not determined.
        """

        mgr = CredentialManager()

        with self.assertRaises(CredentialException) as exc_info:
            mgr._resolve_credential_topic(
                credential_def_spec.copy(), self.processor_config
            )

        assert (
            "Topic source_id or type could not be determined from the processor config."
            in str(exc_info.exception)
        )

    def test_resolve_credential_topic_not_found(self, *_):
        """Test the _resolve_credential_topic function raises an error: topic not found."""

        mgr = CredentialManager()

        with self.assertRaises(CredentialException) as exc_info:
            mgr._resolve_credential_topic(
                credential_def_spec.copy(), self.processor_config
            )

        assert (
            f"Topic with source_id 'A0131571' and type 'registration.registries.ca' does not exist."
            in str(exc_info.exception)
        )

    def test_process_mapping(self):
        """Test the _process_mapping function returns a value from the credential data."""

        test_data = {
            "raw_data": {
                "deeply": {"nested": {"value": "test value"}},
            }
        }
        rule = {"path": "$.deeply.nested.value"}

        mgr = CredentialManager()
        value = mgr._process_mapping(rule, test_data)

        assert value == "test value"

    def test_process_mapping_no_rule(self):
        """Test the _process_mapping function returns None when no rule is provided."""

        test_data = {
            "raw_data": {
                "deeply": {"nested": {"value": "test value"}},
            }
        }
        rule = {"path": None}

        mgr = CredentialManager()
        value = mgr._process_mapping(rule, test_data)

        assert value is None

    def test_process_mapping_no_data(self):
        """Test the _process_mapping function returns None when no data is supplied."""

        test_data = None
        rule = {"path": "$.deeply.nested.value"}

        mgr = CredentialManager()
        value = mgr._process_mapping(rule, test_data)

        assert value is None

    def test_process_mapping_no_raw_data(self):
        """Test the _process_mapping function returns None when no raw data is supplied."""

        test_data = {"raw_data": None}
        rule = {"path": "$.deeply.nested.value"}

        mgr = CredentialManager()
        value = mgr._process_mapping(rule, test_data)

        assert value is None

    def test_process_mapping_no_match(self):
        """Test the _process_mapping function returns None when no match is found."""

        test_data = {
            "raw_data": {
                "deeply": {"nested": {"value": "test value"}},
            }
        }
        rule = {"path": "$.deeply.nested.another_value"}

        mgr = CredentialManager()
        value = mgr._process_mapping(rule, test_data)

        assert value is None

    def test_process_config_date_effective_date(self):
        """Test the _process_config_date function returns the effective date from the credential data."""

        config = self.processor_config.get("credential")

        mgr = CredentialManager()
        test_date = mgr._process_config_date(
            config, credential_def_spec.copy(), "effective_date"
        )
        # Effective date is 2024-08-12T05:44:20+00:00
        assert test_date == datetime(2024, 8, 12, 0, 0, 0, 0, timezone.utc)

    def test_process_config_date_revoked_date(self):
        """Test the _process_config_date function returns the revoked date from the credential data."""

        config = self.processor_config.get("credential")

        mgr = CredentialManager()
        test_date = mgr._process_config_date(
            config, credential_def_spec.copy(), "revoked_date"
        )
        # Effective date is 2025-08-12T05:44:20+00:00
        assert test_date == datetime(2025, 8, 12, 0, 0, 0, 0, timezone.utc)

    def test_process_config_date_none(self):
        """Test the _process_config_date function returns no date from the credential data."""

        config = self.processor_config.get("credential")

        mgr = CredentialManager()
        test_date = mgr._process_config_date(
            config, credential_def_spec.copy(), "invalid_date"
        )
        assert test_date is None

    def test_process_credential_properties(self):
        """Test the _process_credential_properties function returns a dictionary of credential data."""

        mgr = CredentialManager()
        credential_data = mgr._process_credential_properties(
            credential_def_spec.copy(), self.processor_config
        )

        assert credential_data is not None
        assert credential_data.get("credential_id") == credential_def_spec.get(
            "credential_id"
        )
        assert credential_data.get("effective_date") is not None
        assert credential_data.get("revoked_date") is None
        assert credential_data.get("revoked") is False

    @patch(
        "agent_webhooks.utils.vc_di_credential.CredentialManager._set_additional_properties",
    )
    @patch("api.v2.models.Topic.objects.get", autospec=True)
    @patch(
        "agent_webhooks.utils.vc_di_credential.CredentialManager._resolve_credential_type"
    )
    def test_update_credential(
        self,
        mock_resolve_credential_type,
        mock_topic_get,
        mock_set_additional_properties,
    ):
        """Test the update_credential function updates the credential data."""

        credential_type = CredentialType.objects.get(
            issuer=self.issuer, schema=self.schema
        )

        credential_type.processor_config = self.processor_config
        mock_resolve_credential_type.return_value = credential_type

        mock_topic = Topic(source_id="A0131571", type="registration.registries.ca")
        mock_topic.save()
        mock_topic_get.return_value = mock_topic

        mgr = CredentialManager()

        # We have to ensure raw_data is set to None
        mock_set_additional_properties.return_value = {
            "format": credential_def_spec.get("format"),
        }

        # Create a new credential
        credential = mgr.update_credential(credential_def_spec.copy())

        assert credential.credential_id == "203296ac-6d8f-4988-9d7f-d23d3ca36db4"
        assert credential.effective_date == datetime(
            2024, 8, 12, 0, 0, 0, 0, timezone.utc
        )
        assert credential.revoked_date == None
        assert credential.revoked == False

        assert credential.all_attributes is not None
        print(len(credential.all_attributes))
        # assert len(credential.all_attributes) == 2
