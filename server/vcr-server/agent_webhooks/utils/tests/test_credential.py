from datetime import datetime, timezone
import json

from django.test import TestCase
from unittest.mock import patch

from agent_webhooks.utils import credential


class Credential_TestCase(TestCase):
    def test_load(self):
        test_cred_data = {
            "thread_id": "thread-12345-67890",
            "schema_id": "schema-origin-did:2:schema-name:schema-version",
            "cred_def_id": "origin-did:1:2:3",
            "rev_reg_id": "rev reg id",
            "attrs": {"attr": "attr-value"},
        }
        test_cred = credential.Credential(test_cred_data, None)
        assert test_cred.raw == test_cred_data
        assert test_cred.schema_origin_did == "schema-origin-did"
        assert test_cred.origin_did == "origin-did"
        assert json.loads(test_cred.json) == test_cred_data
        assert test_cred.schema_name == "schema-name"
        assert test_cred.schema_version == "schema-version"
        assert test_cred.claim_attributes == ["attr"]
        assert test_cred.cred_def_id == test_cred_data["cred_def_id"]
        assert test_cred.attr == "attr-value"


class CredentialManager_TestCase(TestCase):
    def test_process_mapping(self):
        test_cred = credential.Credential(
            {
                "thread_id": "thread-12345-67890",
                "schema_id": "schema id",
                "cred_def_id": "not:a:did:987654",
                "rev_reg_id": "rev reg id",
                "attrs": {"attr": "attr-value"},
            },
            None,
        )
        test_value_mapping = {"input": "test-value", "from": "value"}
        test_claim_mapping = {"input": "attr", "from": "claim"}
        test_processor_mapping = {
            "input": "test-value",
            "from": "value",
            "processor": ["string_helpers.uppercase"],
        }

        mgr = credential.CredentialManager()
        assert mgr.process_mapping(test_value_mapping, test_cred) == "test-value"
        assert mgr.process_mapping(test_claim_mapping, test_cred) == "attr-value"
        assert mgr.process_mapping(test_processor_mapping, test_cred) == "TEST-VALUE"

    def test_resolve_topic(self):
        test_cred = credential.Credential(
            {
                "thread_id": "thread-12345-67890",
                "schema_id": "schema id",
                "cred_def_id": "not:a:did:987654",
                "rev_reg_id": "rev reg id",
                "attrs": {"topic_id": "topic-source-id"},
            },
            None,
        )
        pconfig = {
            "topic": [
                {
                    "source_id": {"input": "topic_id", "from": "claim"},
                    "type": {"input": "topic-type", "from": "value"},
                    "related_source_id": {
                        "input": "related-source-id",
                        "from": "value",
                    },
                    "related_type": {"input": "related-type", "from": "value"},
                }
            ]
        }

        mgr = credential.CredentialManager()
        (
            topic,
            related_topic,
            topic_created,
            related_topic_created,
        ) = mgr.resolve_credential_topics(test_cred, pconfig)
        assert topic.source_id == "topic-source-id"
        assert topic.type == "topic-type"
        assert topic_created
        assert related_topic.source_id == "related-source-id"
        assert related_topic.type == "related-type"
        assert related_topic_created

    def test_cardinality(self):
        test_cred = credential.Credential(
            {
                "thread_id": "thread-12345-67890",
                "schema_id": "schema id",
                "cred_def_id": "not:a:did:987654",
                "rev_reg_id": "rev reg id",
                "attrs": {
                    "topic_id": "topic-source-id",
                    "effective_date": "eff-date",
                    "etc": "more",
                },
            },
            None,
        )
        pconfig = {"cardinality_fields": ["topic_id", "effective_date"]}

        mgr = credential.CredentialManager()
        cardinal = mgr.credential_cardinality(test_cred, pconfig)
        assert cardinal == {
            "values": {"topic_id": "topic-source-id", "effective_date": "eff-date"},
            "hash": b"Vexy8NBqP5g1W3JLBbVLhErCXNjtLnS4gZGekur/ojI=",
        }

    def test_config_date(self):
        test_cred = credential.Credential(
            {
                "thread_id": "thread-12345-67890",
                "schema_id": "schema id",
                "cred_def_id": "not:a:did:987654",
                "rev_reg_id": "rev reg id",
                "attrs": {"effective_date": "2000-01-01 12:00:00", "etc": "more"},
            },
            None,
        )
        mapping = {"eff_date": {"input": "effective_date", "from": "claim"}}

        mgr = credential.CredentialManager()
        test_date = mgr.process_config_date(mapping, test_cred, "eff_date")
        assert test_date == datetime(2000, 1, 1, 12, 0, 0, 0, timezone.utc)

    def test_credential_props(self):
        test_cred = credential.Credential(
            {
                "thread_id": "thread-12345-67890",
                "schema_id": "schema id",
                "cred_def_id": "not:a:did:987654",
                "rev_reg_id": "rev reg id",
                "attrs": {
                    "eff_date": "2000-01-01 12:00:00",
                    "rev_date": "2001-01-01 12:00:00",
                    "etc": "more",
                },
            },
            None,
        )
        pconfig = {
            "credential": {
                "effective_date": {"input": "eff_date", "from": "claim"},
                "revoked_date": {"input": "rev_date", "from": "claim"},
                "inactive": {"input": "1", "from": "value"},
            }
        }

        mgr = credential.CredentialManager()
        props = mgr.process_credential_properties(test_cred, pconfig)
        print(props)
        assert props == {
            "effective_date": datetime(2000, 1, 1, 12, 0, 0, 0, timezone.utc),
            "inactive": True,
            "revoked_date": datetime(2001, 1, 1, 12, 0, 0, 0, timezone.utc),
            "revoked": True,
        }
