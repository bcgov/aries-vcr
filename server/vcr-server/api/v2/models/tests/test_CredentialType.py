from django.test import TestCase

from api.v2.models.CredentialType import CredentialType


class CredentialType_TestCase(TestCase):
    def test_tagged_attributes(self):
        test_pconfig = {
            "credential": {"effective_date": {"input": "eff_date", "from": "claim"}},
            "topic": [{"source_id": {"input": "topic_id", "from": "claim"}}],
            "cardinality_fields": ["card_1", "card_2"],
        }

        ctype = CredentialType()
        ctype.processor_config = test_pconfig

        attrs = list(ctype.get_tagged_attributes())
        attrs.sort()
        assert attrs == ["card_1", "card_2", "eff_date", "topic_id"]
