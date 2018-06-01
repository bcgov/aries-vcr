import json as _json
import logging

from api.indy.agent import Holder
from api.indy import eventloop

from von_agent.util import schema_key

from api_v2.models.Issuer import Issuer
from api_v2.models.Schema import Schema
from api_v2.models.Subject import Subject
from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.CredentialType import CredentialType
from api_v2.models.Claim import Claim

logger = logging.getLogger(__name__)


class CredentialException(Exception):
    pass


class Credential(object):
    """An python-idiomatic representation of an indy credential
    
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
        # TODO: use credential processor mapping to populate search
        #       database further
        eventloop.do(self.store(legal_entity_id))

    def populate_application_database(self, legal_entity_id):
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

    async def store(self, legal_entity_id):

        # Store credential in wallet
        async with Holder(legal_entity_id) as holder:
            await holder.store_cred(
                self.credential.json,
                _json.dumps(self.credential_definition_metadata),
            )
