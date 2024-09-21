from django.urls import reverse
from rest_framework.test import APITestCase

from api.v2.models import Credential, CredentialType, Issuer, Schema, Topic


class TestRestViewCredential(APITestCase):
    def setUp(self) -> None:
        """Add a test credential type and credential to the database."""

        self.test_credential_type = CredentialType(
            schema=Schema.objects.create(
                name="test_schema", version="0.0.1", origin_did="a:did:123"
            ),
            issuer=Issuer.objects.create(
                did="a:did:123",
                name="Test Issuer 1",
                abbreviation="TI-1",
                email="",
                url="",
            ),
        )
        self.test_credential_type.save()

        self.test_topic = Topic(source_id="test_source_id", type="test_topic_type")
        self.test_topic.save()

        self.test_credential = Credential(
            credential_id="test_credential",
            credential_type=self.test_credential_type,
            topic=self.test_topic,
        )
        self.test_credential.save()

    def test_get_credential(self):
        """Test that the API returns the correct credential data."""
        response = self.client.get("/api/v4/credential/test_credential")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("credential_id"), "test_credential")
        self.assertEqual(
            response.data.get("credential_type"), self.test_credential_type.id
        )
        self.assertIn("attributes", response.data)
        self.assertIn("names", response.data)

    def test_get_credential_raw(self):
        """Test that the API returns the correct credential data when raw_data is requested"""
        response = self.client.get("/api/v4/credential/test_credential?raw_data=true")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})
        self.assertNotIn("credential_id", response.data)
        self.assertNotIn("credential_type", response.data)
        self.assertNotIn("attributes", response.data)
        self.assertNotIn("names", response.data)
