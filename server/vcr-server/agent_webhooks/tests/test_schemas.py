from django.test import TestCase
from marshmallow import ValidationError

from agent_webhooks.schemas import (
    CredentialMappingDefSchema,
    IssuerDefSchema,
    IssuerRegistrationDefSchema,
    MappingDefSchema,
    TopicDefSchema,
    CredentialTypeDefSchema,
    CredentialTypeRegistrationDefSchema,
)
from agent_webhooks.tests.data import (
    credential_type_def_spec,
    effective_date_credential_mapping_def_spec,
    expiry_date_credential_mapping_def_spec,
    effective_date_mapping_def_spec,
    issuer_def_spec,
    topic_def_spec,
)


class TestTopicDefSchema(TestCase):
    def test_valid_topic_def(self):
        """Test the TopicDefSchema with valid data"""

        test_data = topic_def_spec.copy()

        schema = TopicDefSchema()
        result = schema.load(test_data)

        assert "type" in result
        assert result.get("type") == topic_def_spec.get("type")
        assert "source_id" in result
        assert result.get("source_id") == topic_def_spec.get("source_id")

        source_id = result.get("source_id")

        assert "path" in source_id
        assert source_id.get("path") == topic_def_spec.get("source_id").get("path")

    def test_invalid_topic_def_missing_type(self):
        """Test the TopicDefSchema with invalid data - missing type"""

        test_data = topic_def_spec.copy()
        del test_data["type"]

        schema = TopicDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "type" in exc_info.exception.messages
        message = exc_info.exception.messages.get("type")
        assert "Missing data for required field." in message

    def test_invalid_topic_def_missing_source_id(self):
        """Test the TopicDefSchema with invalid data - missing source_id"""

        test_data = topic_def_spec.copy()
        del test_data["source_id"]

        schema = TopicDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "source_id" in exc_info.exception.messages
        message = exc_info.exception.messages.get("source_id")
        assert "Missing data for required field." in message

    def test_invalid_topic_def_missing_source_id_path(self):
        """Test the TopicDefSchema with invalid data - missing source_id path"""

        test_data = {
            **topic_def_spec.copy(),
            "source_id": {},
        }

        schema = TopicDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "source_id" in exc_info.exception.messages
        message = exc_info.exception.messages.get("source_id")
        assert "path" in message
        path_message = message.get("path")
        assert "Missing data for required field." in path_message

    def test_invalid_topic_def_source_id_invalid_source_id(self):
        """Test the TopicDefSchema with invalid data - invalid source_id"""

        test_data = {**topic_def_spec.copy(), "source_id": "invalid-path"}

        schema = TopicDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "source_id" in exc_info.exception.messages
        message = exc_info.exception.messages.get("source_id")
        assert "_schema" in message
        schema_message = message.get("_schema")
        assert "Invalid input type." in schema_message

    def test_invalid_topic_def_source_id_invalid_source_id_path(self):
        """Test the TopicDefSchema with invalid data - invalid source_id path"""

        test_data = {**topic_def_spec.copy(), "source_id": {"path": 123}}

        schema = TopicDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "source_id" in exc_info.exception.messages
        message = exc_info.exception.messages.get("source_id")
        assert "path" in message
        path_message = message.get("path")
        assert "Not a valid string." in path_message


class TestMappingDefSchema(TestCase):
    def test_valid_mapping_def(self):
        """Test the MappingDefSchema with valid data"""

        test_data = effective_date_mapping_def_spec.copy()

        schema = MappingDefSchema()
        result = schema.load(test_data)

        assert "type" in result
        assert result.get("type") == test_data.get("type")
        assert "name" in result
        assert result.get("name") == test_data.get("name")
        assert "path" in result
        assert result.get("path") == test_data.get("path")

    def test_invalid_mapping_def_missing_type(self):
        """Test the MappingDefSchema with invalid data - missing type"""

        test_data = effective_date_mapping_def_spec.copy()
        del test_data["type"]

        schema = MappingDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "type" in exc_info.exception.messages
        message = exc_info.exception.messages.get("type")
        assert "Missing data for required field." in message

    def test_invalid_mapping_def_missing_name(self):
        """Test the MappingDefSchema with invalid data - missing name"""

        test_data = effective_date_mapping_def_spec.copy()
        del test_data["name"]

        schema = MappingDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "name" in exc_info.exception.messages
        message = exc_info.exception.messages.get("name")
        assert "Missing data for required field." in message

    def test_invalid_mapping_def_missing_path(self):
        """Test the MappingDefSchema with invalid data - missing path"""

        test_data = effective_date_mapping_def_spec.copy()
        del test_data["path"]

        schema = MappingDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "path" in exc_info.exception.messages
        message = exc_info.exception.messages.get("path")
        assert "Missing data for required field." in message

    def test_invalid_mapping_def_bad_type_mapping(self):
        """Test the MappingDefSchema with invalid data - bad type mapping"""

        test_data = {**effective_date_mapping_def_spec.copy(), "type": "invalid-type"}

        schema = MappingDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "type" in exc_info.exception.messages
        message = exc_info.exception.messages.get("type")
        assert "Must be one of: effective_date, expiry_date, revoked_date." in message


class TestCredentialMappingDefSchema(TestCase):
    def test_valid_credential_mapping_def(self):
        """Test the CredentialMappingDefSchema with valid data"""

        test_data = effective_date_credential_mapping_def_spec.copy()

        schema = CredentialMappingDefSchema()
        result = schema.load(test_data)

        assert "type" not in result
        assert "name" in result
        assert result.get("name") == test_data.get("name")
        assert "path" in result
        assert result.get("path") == test_data.get("path")


class TestCredentialTypeDef(TestCase):
    def test_valid_credential_type_def(self):
        """Test the CredentialTypeDefSchema with valid data"""

        test_data = credential_type_def_spec.copy()

        schema = CredentialTypeDefSchema()
        result = schema.load(test_data)

        assert "format" in result
        assert result.get("format") == test_data.get("format")
        assert "schema" in result
        assert result.get("schema") == test_data.get("schema")
        assert "version" in result
        assert result.get("version") == test_data.get("version")
        assert "origin_did" in result
        assert result.get("origin_did") == test_data.get("origin_did")
        assert "topic" in result
        assert "mappings" in result
        assert "credential" in result

        mappings = result.get("mappings")
        credential = result.get("credential")

        assert len(mappings) == 2
        assert "effective_date" in credential
        assert "revoked_date" in credential

        effective_date = credential.get("effective_date")
        revoked_date = credential.get("revoked_date")

        assert effective_date == effective_date_credential_mapping_def_spec
        assert revoked_date == expiry_date_credential_mapping_def_spec

    def test_valid_credential_type_no_mappings(self):
        """Test the CredentialTypeSchema with valid data - no mappings"""

        test_data = credential_type_def_spec.copy()
        del test_data["mappings"]

        exception_raised = False
        try:
            schema_no_mappings = CredentialTypeDefSchema()
            schema_no_mappings.load(test_data)
        except ValidationError:
            exception_raised = True

        assert not exception_raised

    def test_valid_credential_type_empty_mappings(self):
        """Test the CredentialTypeSchema with valid data - empty mappings"""

        test_data = {
            **credential_type_def_spec.copy(),
            "mappings": [],
        }

        exception_raised = False
        try:
            schema_empty_mappings = CredentialTypeDefSchema()
            schema_empty_mappings.load(test_data)
        except ValidationError:
            exception_raised = True

        assert not exception_raised

    def test_invalid_credential_type_invalid_format(self):
        """Test the CredentialTypeSchema with invalid data - invalid format"""

        test_data = {
            **credential_type_def_spec.copy(),
            "format": "invalid-format",
        }

        schema = CredentialTypeDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "format" in exc_info.exception.messages
        message = exc_info.exception.messages.get("format")
        assert "Must be one of: vc_di, anoncreds." in message


class TestIssuerDef(TestCase):
    def test_valid_issuer_def(self):
        """Test the IssuerDefSchema with valid data"""

        test_data = issuer_def_spec.copy()

        schema = IssuerDefSchema()
        result = schema.load(test_data)

        assert "name" in result
        assert result.get("name") == test_data.get("name")
        assert "did" in result
        assert result.get("did") == test_data.get("did")
        assert "abbreviation" in result
        assert result.get("abbreviation") == test_data.get("abbreviation")
        assert "email" in result
        assert result.get("email") == test_data.get("email")
        assert "url" in result
        assert result.get("url") == test_data.get("url")

    def test_invalid_issuer_def_missing_name(self):
        """Test the IssuerDefSchema with invalid data - missing name"""

        test_data = issuer_def_spec.copy()
        del test_data["name"]

        schema = IssuerDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "name" in exc_info.exception.messages
        message = exc_info.exception.messages.get("name")
        assert "Missing data for required field." in message

    def test_invalid_issuer_def_invalid_name(self):
        """Test the IssuerDefSchema with invalid data - invalid name"""

        test_data = {**issuer_def_spec.copy(), "name": 123}

        schema = IssuerDefSchema()

        with self.assertRaises(ValidationError) as exc_info:
            schema.load(test_data)

        assert "name" in exc_info.exception.messages
        message = exc_info.exception.messages.get("name")
        assert "Not a valid string." in message


class TestIssuerRegistrationDef(TestCase):
    def test_valid_issuer_registration_def(self):
        """Test the IssuerRegistrationDefSchema with valid data"""

        test_data = {
            "issuer": issuer_def_spec.copy(),
        }

        schema = IssuerRegistrationDefSchema()
        result = schema.load(test_data)

        assert "issuer" in result

        issuer = result.get("issuer")

        assert issuer == issuer_def_spec

        result = schema.dump(result)

        assert "issuer_registration" in result

        issuer_registration = result.get("issuer_registration")
        assert "issuer" in issuer_registration


class TestCredentialTypeRegistrationDef(TestCase):
    def test_valid_credential_type_registration_def(self):
        """Test the CredentialTypeRegistrationDefSchema with valid data"""

        test_data = {
            "issuer": issuer_def_spec.copy(),
            "credential_type": credential_type_def_spec.copy(),
        }

        schema = CredentialTypeRegistrationDefSchema()
        result = schema.load(test_data)

        assert "issuer" in result
        assert "credential_type" in result

        issuer = result.get("issuer")
        credential_type = result.get("credential_type")

        assert issuer == issuer_def_spec
        assert credential_type == credential_type_def_spec

        result = schema.dump(result)

        assert "issuer_registration" in result

        issuer_registration = result.get("issuer_registration")
        assert "credential_type" not in issuer_registration
        assert "issuer" in issuer_registration
        assert "credential_types" in issuer_registration
        assert len(issuer_registration.get("credential_types")) == 1
