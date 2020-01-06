from django.test import TestCase
from unittest.mock import patch

from agent_webhooks.utils import issuer


class IssuerManager_TestCase(TestCase):

    # Note: saving to JSONField is not supported when we use
    # sqlite as the back-end (in testing)
    @patch("api_v2.models.CredentialType.save", autospec=True)
    def test_issuer_registration(self, mock_cred_type_save):
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
                        "mapping": {},
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

        assert len(result.credential_types) == 1
        ctype = result.credential_types[0]
        assert ctype.description == "cred type name"
        assert ctype.processor_config == {
            "cardinality_fields": ["field"],
            "credential": {"effective_date": {"input": "eff_date", "from": "claim"}},
            "mapping": {},
            "topic": [{"source_id": {"input": "topic_id", "from": "claim"}}],
        }
