from django.test import TestCase
from unittest.mock import patch

from api.v2.models.Issuer import Issuer

from agent_webhooks.tests.data import credential_type_def_spec, issuer_def_spec
from agent_webhooks.utils import schema


class TestSchemaManager(TestCase):
    """
    Test the SchemaManager class
    """

    @patch("api.v2.models.Schema.save", autospec=True)
    def test_schema_registration(self, mock_schema_save):

        test_issuer_data = issuer_def_spec.copy()
        test_data = [credential_type_def_spec.copy()]

        mgr = schema.SchemaManager()
        test_issuer = Issuer(**test_issuer_data)
        test_issuer.save()
        result = mgr.update_schemas(test_issuer, test_data)

        mock_schema_save.assert_called()
        assert len(result) == 1

        saved_schema = result[0]

        assert saved_schema.name == credential_type_def_spec.get("schema")
        assert saved_schema.version == credential_type_def_spec.get("version")
        assert saved_schema.origin_did == test_issuer.did
