import json as _json
import logging
from importlib import import_module

from api.indy.agent import Holder
from api.indy import eventloop

from von_agent.util import schema_key

from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.models.Subject import Subject
from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Claim import Claim

from api_v2.models.Name import Name
from api_v2.models.Address import Address
from api_v2.models.Person import Person
from api_v2.models.Contact import Contact

logger = logging.getLogger(__name__)

PROCESSOR_FUNCTION_BASE_PATH = "api_v2.processor"

SUPPORTED_MODELS_MAPPING = {
    "name": Name,
    "address": Address,
    "person": Person,
    "contact": Contact,
}


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
    def __init__(
        self, credential: Credential, credential_definition_metadata: dict
    ) -> None:
        self.credential = credential
        self.credential_definition_metadata = credential_definition_metadata

    def process(self):
        # Legal entity id is required
        # TODO: Allow issuer to specify source id claim attribute name
        #       for now, we expect legal_entity_id
        try:
            legal_entity_id = self.credential.legal_entity_id
        except AttributeError as e:
            raise CredentialException(
                "Credential does not contain a claim named 'legal_entity_id'"
            )

        self.populate_application_database(legal_entity_id)
        eventloop.do(self.store(legal_entity_id))

    def populate_application_database(self, legal_entity_id):
        # Obtain required models from database
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

        # Create subject, credential, claim models
        subject, created = Subject.objects.get_or_create(
            source_id=legal_entity_id
        )

        credential = CredentialModel.objects.create(
            subject=subject, credential_type=credential_type
        )

        # TODO: optimize into a single insert
        for claim_attribute in self.credential.claim_attributes:
            claim_value = getattr(self.credential, claim_attribute)
            Claim.objects.create(
                credential=credential, name=claim_attribute, value=claim_value
            )

        # Update optional models based on processor config
        processor_config = credential_type.processor_config
        if not processor_config:
            return

        processor_config = _json.loads(processor_config)

        processor_config = [
            {
                "model": "name",
                "fields": {
                    "text": {"input": "legal_name", "from": "claim"},
                    "type": {"input": "legal_name", "from": "value"}
                }
            },
            {
                "model": "address",
                "fields": {
                    "addressee": {"input": "addressee", "from": "claim"},
                    "civic_address": {
                        "input": "address_line_1",
                        "from": "claim"
                    },
                    "city": {"input": "city", "from": "claim"},
                    "province": {"input": "province", "from": "claim"},
                    "postal_code": {"input": "postal_code", "from": "claim"},
                    "country": {"input": "country", "from": "claim"},
                    "address_type": {"input": "operating", "from": "value"}
                }
            },
            {
                "model": "address",
                "fields": {
                    "addressee": {"input": "addressee", "from": "claim"},
                    "civic_address": {
                        "input": "address_line_1",
                        "from": "claim",
                        "processor": [
                            "string_helpers.uppercase",
                            "string_helpers.to_string",
                            "string_helper.lowercase"
                        ]
                    },
                    "city": {"input": "city", "from": "claim"},
                    "province": {"input": "province", "from": "claim"},
                    "postal_code": {"input": "postal_code", "from": "claim"},
                    "country": {"input": "country", "from": "claim"},
                    "address_type": {"input": "operating", "from": "value"}
                }
            }
        ]

        # Iterate model types in processor mapping
        for i, model_mapper in enumerate(processor_config):
            model_name = model_mapper["model"]

            # We currently support 4 model types
            # see SUPPORTED_MODELS_MAPPING
            try:
                Model = SUPPORTED_MODELS_MAPPING[model_name]
            except KeyError as error:
                raise CredentialException(
                    "Unsupported model type '{}'".format(model_name)
                )

            model = Model()

            # Iterate fields on model mapping config
            for field in processor_config[i]["fields"]:
                field_data = processor_config[i]["fields"][field]

                # Get required values from config
                try:
                    _input = field_data["input"]
                    _from = field_data["from"]
                except KeyError as error:
                    raise CredentialException(
                        "Every field must specify 'input' and 'from' values."
                    )

                # Pocessor is optional
                try:
                    processor = field_data["processor"]
                except KeyError as error:
                    processor = None

                # Get model field value from string literal or claim value
                if _from == "value":
                    field_value = _input
                elif _from == "claim":
                    field_value = getattr(self.credential, _input)
                else:
                    raise CredentialException(
                        "Supported field from values are 'value' and 'claim'"
                        + " but received '{}'".format(_from)
                    )

                # If we have a processor config, build pipeline of functions
                # and run field value through pipeline
                if processor is not None:
                    pipeline = []
                    # Construct pipeline
                    for function_path_with_name in processor:
                        function_path, function_name = function_path_with_name.rsplit(
                            ".", 1
                        )

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

                        try:
                            function = getattr(function_module, function_name)
                        except AttributeError as error:
                            raise CredentialException(
                                "Module '{}' has no function '{}'.".format(
                                    function_path, function_name
                                )
                            )

                        pipeline.append(function)

                    # We want to run the pipeline in logical order
                    pipeline.reverse()

                    # Run pipeline
                    while len(pipeline) > 0:
                        function = pipeline.pop()
                        field_value = function(field_value)

                # Set value on model field
                setattr(model, field, field_value)

            model.save()

    async def store(self, legal_entity_id):

        # Store credential in wallet
        async with Holder(legal_entity_id) as holder:
            await holder.store_cred(
                self.credential.json,
                _json.dumps(self.credential_definition_metadata),
            )
