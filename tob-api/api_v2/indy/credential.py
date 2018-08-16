import json as _json
import logging
from importlib import import_module

from django.utils import timezone

from api.indy.agent import Holder
from api.indy import eventloop

from von_agent.util import schema_key

from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.models.Topic import Topic
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.Claim import Claim

from api_v2.models.Name import Name
from api_v2.models.Address import Address
from api_v2.models.Person import Person
from api_v2.models.Contact import Contact
from api_v2.models.Category import Category

logger = logging.getLogger(__name__)

PROCESSOR_FUNCTION_BASE_PATH = "api_v2.processor"

SUPPORTED_MODELS_MAPPING = {
    "name": Name,
    "address": Address,
    "person": Person,
    "contact": Contact,
    "category": Category,
}

SUPPORTED_CATEGORIES = ["topic_status", "topic_type"]

# TODO: Allow issuer to dynamically register topic types
# Currently we only support 2 topic types. We only understand
# a predefined relationship: incorporation --< doing_business_as
SUPPORTED_TOPIC_TYPES = ["incorporation", "doing_business_as", "registration"]


class CredentialException(Exception):
    pass


class Credential(object):
    """A python-idiomatic representation of an indy credential
    
    Claim values are made available as class members.

    for example:

    ```json
    "postal_code": {
        "raw": "N2L 6P3",
        "encoded": "1062703188233012330691500488799027"
    }
    ```

    becomes:

    ```python
    self.postal_code = "N2L 6P3"
    ```

    on the class object.

    Arguments:
        credential_data {object} -- Valid credential data as sent by an issuer
    """

    def __init__(self, credential_data: object) -> None:
        self._raw = credential_data
        self._schema_id = credential_data["schema_id"]
        self._cred_def_id = credential_data["cred_def_id"]
        self._rev_reg_id = credential_data["rev_reg_id"]
        self._signature = credential_data["signature"]
        self._signature_correctness_proof = credential_data[
            "signature_correctness_proof"
        ]
        self._rev_reg = credential_data["rev_reg"]
        self._witness = credential_data["witness"]

        self._claim_attributes = []

        # Parse claim attributes into array
        # Values are available as class attributes
        claim_data = credential_data["values"]
        for claim_attribute in claim_data:
            self._claim_attributes.append(claim_attribute)

    def __getattr__(self, name: str):
        """Make claim values accessible on class instance"""
        try:
            claim_value = self.raw["values"][name]["raw"]
            return claim_value
        except KeyError:
            raise AttributeError(
                "'Credential' object has no attribute '{}'".format(name)
            )

    @property
    def raw(self) -> dict:
        """Accessor for raw credential data
        
        Returns:
            dict -- Python dict representation of raw credential data
        """
        return self._raw

    @property
    def json(self) -> str:
        """Accessor for json credential data
        
        Returns:
            str -- JSON representation of raw credential data
        """
        return _json.dumps(self._raw)

    @property
    def origin_did(self) -> str:
        """Accessor for schema origin did
        
        Returns:
            str -- origin did
        """
        return schema_key(self._schema_id).origin_did

    @property
    def schema_name(self) -> str:
        """Accessor for schema name
        
        Returns:
            str -- schema name
        """
        return schema_key(self._schema_id).name

    @property
    def schema_version(self) -> str:
        """Accessor for schema version
        
        Returns:
            str -- schema version
        """
        return schema_key(self._schema_id).version

    @property
    def claim_attributes(self) -> list:
        """Accessor for claim attributes
        
        Returns:
            list -- claim attributes
        """
        return self._claim_attributes


class CredentialManager(object):
    """
    Handles processing of incoming credentials. Populates application
    database based on rules provided by issuer are registration.
    """

    def __init__(
        self, credential: Credential, credential_definition_metadata: dict
    ) -> None:
        self.credential = credential
        self.credential_definition_metadata = credential_definition_metadata

    def process(self):
        """
        Processes incoming credential data and returns newly created credential
        
        Returns:
            Credential -- newly created credential in application database
        """
        # Get context for this credential if it exists
        try:
            issuer = Issuer.objects.get(did=self.credential.origin_did)
            schema = Schema.objects.get(
                origin_did=self.credential.origin_did,
                name=self.credential.schema_name,
                version=self.credential.schema_version,
            )
        except Issuer.DoesNotExist:
            raise CredentialException(
                "Issuer with did '{}' does not exist.".format(
                    self.credential.origin_did
                )
            )
        except Schema.DoesNotExist:
            raise CredentialException(
                "Schema with origin_did"
                + " '{}', name '{}', and version '{}' ".format(
                    self.credential.origin_did,
                    self.credential.schema_name,
                    self.credential.schema_version,
                )
                + " does not exist."
            )

        credential_type = CredentialType.objects.get(
            schema=schema, issuer=issuer
        )

        credential_wallet_id = eventloop.do(self.store())
        self.populate_application_database(
            credential_type, credential_wallet_id
        )

        return credential_wallet_id

    def populate_application_database(
        self, credential_type, credential_wallet_id
    ):

        # Takes our mapping rules and returns a value from credential
        def process_mapping(rules):
            if not rules:
                return None

            # Get required values from config
            try:
                _input = rules["input"]
                _from = rules["from"]
            except KeyError as error:
                raise CredentialException(
                    "Every mapping must specify 'input' and 'from' values."
                )

            # Pocessor is optional
            try:
                processor = rules["processor"]
            except KeyError as error:
                processor = None

            # Get model field value from string literal or claim value
            if _from == "value":
                mapped_value = _input
            elif _from == "claim":
                try:
                    mapped_value = getattr(self.credential, _input)
                except AttributeError as error:
                    raise CredentialException(
                        "Credential does not contain the configured claim '{}'".format(
                            _input
                        )
                        + "Claims are: {}".format(
                            ", ".join(self.credential.claim_attributes)
                        )
                    )
            else:
                raise CredentialException(
                    "Supported field from values are 'value' and 'claim'"
                    + " but received '{}'".format(_from)
                )

            # If we have a processor config, build pipeline of functions
            # and run field value through pipeline
            if processor is not None:
                pipeline = []
                # Construct pipeline by dot notation. Last token is the
                # function name and all preceeding dots denote path of
                # module starting from `PROCESSOR_FUNCTION_BASE_PATH``
                for function_path_with_name in processor:
                    function_path, function_name = function_path_with_name.rsplit(
                        ".", 1
                    )

                    # Does the file exist?
                    try:
                        function_module = import_module(
                            "{}.{}".format(
                                PROCESSOR_FUNCTION_BASE_PATH, function_path
                            )
                        )
                    except ModuleNotFoundError as error:
                        raise CredentialException(
                            "No processor module named '{}'".format(
                                function_path
                            )
                        )

                    # Does the function exist?
                    try:
                        function = getattr(function_module, function_name)
                    except AttributeError as error:
                        raise CredentialException(
                            "Module '{}' has no function '{}'.".format(
                                function_path, function_name
                            )
                        )

                    # Build up a list of functions to call
                    pipeline.append(function)

                # We want to run the pipeline in logical order
                pipeline.reverse()

                # Run pipeline
                while len(pipeline) > 0:
                    function = pipeline.pop()
                    mapped_value = function(mapped_value)

            # This is ugly. von-agent currently serializes null values
            # to the string 'None'
            if mapped_value == "None":
                mapped_value = None

            return mapped_value

        processor_config = credential_type.processor_config
        topic_defs = processor_config["topic"]

        # We accept object or array for topic def
        if type(topic_defs) is dict:
            topic_defs = [topic_defs]

        cardinality_fields = processor_config.get("cardinality_fields") or []
        mapping = processor_config.get("mapping") or []

        # Issuer can register multiple topic selectors to fall back on
        # We use the first valid topic and related parent if applicable
        for topic_def in topic_defs:
            parent_topic = None
            topic = None

            parent_topic_name = process_mapping(topic_def.get("parent_name"))
            parent_topic_source_id = process_mapping(
                topic_def.get("parent_source_id")
            )
            parent_topic_type = process_mapping(topic_def.get("parent_type"))

            topic_name = process_mapping(topic_def.get("name"))
            topic_source_id = process_mapping(topic_def.get("source_id"))
            topic_type = process_mapping(topic_def.get("type"))

            if (
                topic_type is not None
                and topic_type not in SUPPORTED_TOPIC_TYPES
            ):
                raise CredentialException(
                    "Supported topic types are 'incorporation' and 'doing_business_as' but received topic '{}'".format(
                        topic_type
                    )
                )

            if (
                parent_topic_type is not None
                and parent_topic_type not in SUPPORTED_TOPIC_TYPES
            ):
                raise CredentialException(
                    "Supported topic types are 'incorporation' and 'doing_business_as' but received parent topic '{}'".format(
                        parent_topic_type
                    )
                )

            # Get parent topic if possible
            if parent_topic_name:
                try:
                    parent_topic = Topic.objects.get(
                        credentials__names__text=parent_topic_name
                    )
                except Topic.DoesNotExist:
                    pass
            elif parent_topic_source_id and parent_topic_type:
                try:
                    parent_topic = Topic.objects.get(
                        source_id=parent_topic_source_id,
                        type=parent_topic_type,
                    )
                except Topic.DoesNotExist:
                    pass

            # Current topic if possible
            if topic_name:
                try:
                    topic = Topic.objects.get(
                        credentials__names__text=topic_name
                    )
                except Topic.DoesNotExist:
                    pass
            elif topic_source_id and topic_type:
                # Special Case:
                # Create a new topic if our query comes up empty
                try:
                    topic = Topic.objects.get(
                        source_id=topic_source_id, type=topic_type
                    )
                except Topic.DoesNotExist as error:
                    topic = Topic.objects.create(
                        source_id=topic_source_id, type=topic_type
                    )

            # We stick with the first topic that we resolve
            if topic:
                break

        # If we couldn't resolve _any_ topics from the configuration,
        # we can't continue
        if not topic:
            raise CredentialException(
                "Issuer registration 'topic' must specify at least one valid topic name OR topic type and topic source_id"
            )

        # We search for existing credentials by cardinality_fields to apply end_date
        existing_credential_query = {
            "credential_type__id": credential_type.id,
            "topics__id": topic.id,
            "end_date": None,
        }
        for cardinality_field in cardinality_fields:
            try:
                existing_credential_query["claims__name"] = cardinality_field
                existing_credential_query["claims__value"] = getattr(
                    self.credential, cardinality_field
                )
            except AttributeError as error:
                raise CredentialException(
                    "Issuer configuration specifies field '{}' ".format(
                        cardinality_field
                    )
                    + "in cardinality_fields value does not exist in "
                    + "credential. Values are: {}".format(
                        ", ".join(list(self.credential.claim_attributes))
                    )
                )
        try:
            existing_credential = CredentialModel.objects.get(
                **existing_credential_query
            )
            existing_credential.end_date = timezone.now()
            existing_credential.save()
        except CredentialModel.DoesNotExist as error:
            # No record to implicitly expire
            pass

        # We always create a new credential model to represent the current credential
        credential = topic.credentials.create(
            credential_type=credential_type, wallet_id=credential_wallet_id
        )

        # Create and associate claims for this credential
        for claim_attribute in self.credential.claim_attributes:
            claim_value = getattr(self.credential, claim_attribute)
            Claim.objects.create(
                credential=credential, name=claim_attribute, value=claim_value
            )

        # Recurisvely associate parent topic and all of it's related topics
        # (all related credentials' topics)
        related_topic_ids = []

        def associate_related_topics(topic):
            credential.topics.add(topic)
            for related_credential in topic.credentials.all():
                for credential_topic in related_credential.topics.distinct():
                    # Don't traverse known relationships
                    if credential_topic.id not in related_topic_ids:
                        related_topic_ids.append(credential_topic.id)
                        credential.topics.add(credential_topic)
                        associate_related_topics(credential_topic)

        if parent_topic is not None:
            associate_related_topics(parent_topic)

        # Create search models using mapping from issuer config
        for model_mapper in mapping:
            model_name = model_mapper["model"]

            # We currently support 4 model types
            # see SUPPORTED_MODELS_MAPPING
            try:
                Model = SUPPORTED_MODELS_MAPPING[model_name]
                model = Model()
            except KeyError as error:
                raise CredentialException(
                    "Unsupported model type '{}'".format(model_name)
                )

            for field, field_mapper in model_mapper["fields"].items():
                setattr(model, field, process_mapping(field_mapper))

            # Validate category type
            if (
                model_name == "category"
                and model.type not in SUPPORTED_CATEGORIES
            ):
                raise CredentialException(
                    "Invalid category type '{}'. ".format(model.type)
                    + "Valid categories are: {}".format(
                        ", ".join(list(SUPPORTED_CATEGORIES))
                    )
                )

            model.credential = credential
            model.save()

        return topic

    async def store(self):
        # Store credential in wallet
        async with Holder() as holder:
            return await holder.store_cred(
                self.credential.json,
                _json.dumps(self.credential_definition_metadata),
            )
