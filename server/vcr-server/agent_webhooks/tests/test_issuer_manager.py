from django.test import TestCase
from unittest.mock import patch

from agent_webhooks.tests.data import (
    credential_type_def_spec,
    issuer_def_spec,
    topic_def_spec,
)
from agent_webhooks.utils import issuer


class TestIssuerManager(TestCase):
    """
    Test the IssuerManager class

    Note: saving to JSONField is not supported when we use sqlite as the back-end (in testing)
    """

    test_legacy_data = {
        "issuer_registration": {
            "credential_types": [
                {
                    "category_labels": {"category": "label"},
                    "claim_labels": {"claim": "label"},
                    "claim_descriptions": {"claim": "description"},
                    "credential_def_id": "cred-def-id",
                    "schema": "schema",
                    "name": "cred type name",
                    "version": "version",
                    "credential": {
                        "effective_date": {"input": "eff_date", "from": "claim"}
                    },
                    "topic": [{"source_id": {"input": "topic_id", "from": "claim"}}],
                    "endpoint": "endpoint",
                    "cardinality_fields": ["field"],
                    "mapping": {},
                    "logo_b64": "logo base64",
                }
            ],
            "issuer": {
                "name": "issuer name",
                "did": "issuer-did",
                "abbreviation": "issuer abbrev",
                "email": "issuer email",
                "url": "issuer url",
                "endpoint": "issuer endpoint",
                "logo_b64": "issuer logo base64",
            },
        }
    }

    test_data = {
        "issuer_registration": {
            "credential_types": [
                {
                    **credential_type_def_spec.copy(),
                    "name": "cred type name",
                    "credential_def_id": "cred-def-id",
                    "cardinality_fields": ["field"],
                    "category_labels": {"category": "label"},
                    "claim_labels": {"claim": "label"},
                    "claim_descriptions": {"claim": "description"},
                    "endpoint": "endpoint",
                    "logo_b64": "logo base64",
                }
            ],
            "issuer": issuer_def_spec.copy(),
        }
    }

    @patch("api.v2.models.CredentialType.save", autospec=True)
    @patch("api.v2.models.Schema.save", autospec=True)
    def test_legacy_issuer_registration(
        self, mock_schema_save, mock_credential_type_save
    ):
        mgr = issuer.IssuerManager()

        result = mgr.register_issuer(self.test_legacy_data)
        assert result.issuer.name == "issuer name"
        assert result.issuer.did == "issuer-did"
        assert result.issuer.abbreviation == "issuer abbrev"
        assert result.issuer.email == "issuer email"
        assert result.issuer.endpoint == "issuer endpoint"
        assert result.issuer.logo_b64 == "issuer logo base64"

        mock_schema_save.assert_called()
        mock_credential_type_save.assert_called()

        assert len(result.credential_types) == 1
        assert len(result.schemas) == 1

        schema = result.schemas[0]
        credential_type = result.credential_types[0]

        assert credential_type.description == "cred type name"
        assert credential_type.processor_config == {
            "cardinality": None,
            "cardinality_fields": ["field"],
            "credential": {"effective_date": {"input": "eff_date", "from": "claim"}},
            "mapping": {},
            "mappings": None,
            "topic": [{"source_id": {"input": "topic_id", "from": "claim"}}],
        }
        assert schema.name == "schema"
        assert schema.version == "version"
        assert schema.origin_did == "issuer-did"

    @patch("api.v2.models.CredentialType.save", autospec=True)
    @patch("api.v2.models.Schema.save", autospec=True)
    def test_issuer_registration(self, mock_schema_save, mock_credential_type_save):
        mgr = issuer.IssuerManager()

        result = mgr.register_issuer(self.test_data)
        assert result.issuer.name == issuer_def_spec.get("name")
        assert result.issuer.did == issuer_def_spec.get("did")
        assert result.issuer.abbreviation == issuer_def_spec.get("abbreviation")
        assert result.issuer.email == issuer_def_spec.get("email")
        assert result.issuer.endpoint == issuer_def_spec.get("endpoint")
        assert result.issuer.logo_b64 == issuer_def_spec.get("logo_b64")

        mock_schema_save.assert_called()
        mock_credential_type_save.assert_called()

        assert len(result.credential_types) == 1
        assert len(result.schemas) == 1

        schema = result.schemas[0]
        credential_type = result.credential_types[0]

        assert credential_type.description == "cred type name"
        assert credential_type.processor_config == {
            "cardinality": credential_type_def_spec.get("cardinality"),
            "cardinality_fields": ["field"],
            "credential": credential_type_def_spec.get("credential"),
            "mappings": credential_type_def_spec.get("mappings"),
            "topic": topic_def_spec,
        }
        assert "mapping" not in credential_type.processor_config
        assert schema.name == credential_type_def_spec.get("schema")
        assert schema.version == credential_type_def_spec.get("version")
        assert schema.origin_did == issuer_def_spec.get("did")

    @patch("api.v2.models.CredentialType.save", autospec=True)
    @patch("api.v2.models.Schema.save", autospec=True)
    def test_legacy_issuer_registration_issuer_only(
        self, mock_schema_save, mock_credential_type_save
    ):
        mgr = issuer.IssuerManager()

        result = mgr.register_issuer(self.test_legacy_data, issuer_only=True)
        assert result.issuer.name == "issuer name"
        assert result.issuer.did == "issuer-did"
        assert result.issuer.abbreviation == "issuer abbrev"
        assert result.issuer.email == "issuer email"
        assert result.issuer.endpoint == "issuer endpoint"
        assert result.issuer.logo_b64 == "issuer logo base64"

        mock_schema_save.assert_not_called()
        mock_credential_type_save.assert_not_called()
        assert result.schemas is not None
        assert len(result.schemas) == 0
        assert result.credential_types is not None
        assert len(result.credential_types) == 0

    @patch("api.v2.models.CredentialType.save", autospec=True)
    @patch("api.v2.models.Schema.save", autospec=True)
    def test_issuer_registration_issuer_only(
        self, mock_schema_save, mock_credential_type_save
    ):
        mgr = issuer.IssuerManager()

        result = mgr.register_issuer(self.test_data, issuer_only=True)
        assert result.issuer.name == issuer_def_spec.get("name")
        assert result.issuer.did == issuer_def_spec.get("did")
        assert result.issuer.abbreviation == issuer_def_spec.get("abbreviation")
        assert result.issuer.email == issuer_def_spec.get("email")
        assert result.issuer.endpoint == issuer_def_spec.get("endpoint")
        assert result.issuer.logo_b64 == issuer_def_spec.get("logo_b64")

        mock_schema_save.assert_not_called()
        mock_credential_type_save.assert_not_called()
        assert result.schemas is not None
        assert len(result.schemas) == 0
        assert result.credential_types is not None
        assert len(result.credential_types) == 0
