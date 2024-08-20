from django.test import TestCase
from unittest.mock import patch

from agent_webhooks.utils import issuer


class IssuerManager_TestCase(TestCase):
    # Note: saving to JSONField is not supported when we use sqlite as the back-end (in testing)
    @patch("api.v2.models.CredentialType.save", autospec=True)
    def test_issuer_registration(self, mock_credential_type_save):
        test_spec = {
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
                        "topic": [
                            {"source_id": {"input": "topic_id", "from": "claim"}}
                        ],
                        "endpoint": "endpoint",
                        "cardinality_fields": ["field"],
                        "mappings": {},
                        "visible_fields": "visible,fields",
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

        mgr = issuer.IssuerManager()

        result = mgr.register_issuer(test_spec)
        assert result.issuer.name == "issuer name"
        assert result.issuer.did == "issuer-did"
        assert result.issuer.abbreviation == "issuer abbrev"
        assert result.issuer.email == "issuer email"
        assert result.issuer.endpoint == "issuer endpoint"
        assert result.issuer.logo_b64 == "issuer logo base64"

        mock_credential_type_save.assert_called()

        assert len(result.credential_types) == 1

        credential_type = result.credential_types[0]

        assert credential_type.description == "cred type name"
        assert credential_type.processor_config == {
            "cardinality_fields": ["field"],
            "credential": {"effective_date": {"input": "eff_date", "from": "claim"}},
            "mappings": {},
            "topic": [{"source_id": {"input": "topic_id", "from": "claim"}}],
        }
