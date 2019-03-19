"""Handle credential exchange information interface with non-secrets storage."""

import json
import uuid

from typing import Sequence

from marshmallow import fields

from ....models.base import BaseModel, BaseModelSchema
from ....storage.base import BaseStorage
from ....storage.record import StorageRecord


class CredentialExchange(BaseModel):
    """Represents a credential exchange."""

    class Meta:
        """CredentialExchange metadata."""

        schema_class = "CredentialExchangeSchema"

    RECORD_TYPE = "credential_exchange"

    INITIATOR_SELF = "self"
    INITIATOR_EXTERNAL = "external"

    STATE_OFFER_SENT = "offer_sent"
    STATE_OFFER_RECEIVED = "offer_received"

    def __init__(
        self,
        *,
        credential_exchange_id: str = None,
        initiator: str = None,
        state: str = None,
        credential_definition_id: str = None,
        schema_id: str = None,
        credential_offer: dict = None,
        error_msg: str = None,
    ):
        """Initialize a new CredentialExchange."""
        self._id = credential_exchange_id
        self.initiator = initiator
        self.state = state
        self.credential_definition_id = credential_definition_id
        self.schema_id = schema_id
        self.credential_offer = credential_offer
        self.error_msg = error_msg

    @property
    def credential_exchange_id(self) -> str:
        """Accessor for the ID associated with this exchange."""
        return self._id

    @property
    def storage_record(self) -> StorageRecord:
        """Accessor for a `StorageRecord` representing this credential exchange."""
        return StorageRecord(
            self.RECORD_TYPE,
            json.dumps(self.value),
            self.tags,
            self.credential_exchange_id,
        )

    @property
    def value(self) -> dict:
        """Accessor for the JSON record value generated for this credential exchange."""
        ret = self.tags
        ret.update({"error_msg": self.error_msg})
        return ret

    @property
    def tags(self) -> dict:
        """Accessor for the record tags generated for this credential exchange."""
        result = {}
        for prop in (
            "initiator",
            "state",
            "credential_definition_id",
            "schema_id",
            "credential_offer",
        ):
            val = getattr(self, prop)
            if val:
                result[prop] = val
        return result

    async def save(self, storage: BaseStorage):
        """Persist the credential exchange record to storage.

        Args:
            storage: The `BaseStorage` instance to use
        """
        if not self._id:
            self._id = str(uuid.uuid4())
            await storage.add_record(self.storage_record)
        else:
            record = self.storage_record
            await storage.update_record_value(record, record.value)
            await storage.update_record_tags(record, record.tags)

    @classmethod
    async def retrieve_by_id(
        cls, storage: BaseStorage, credential_exchange_id: str
    ) -> "CredentialExchange":
        """Retrieve a credential exchange record by ID.

        Args:
            storage: The `BaseStorage` instance to use
            credential_exchange_id: The ID of the credential exchange record to find
        """
        result = await storage.get_record(cls.RECORD_TYPE, credential_exchange_id)
        vals = json.loads(result.value)
        if result.tags:
            vals.update(result.tags)
        return CredentialExchange(credential_exchange_id=credential_exchange_id, **vals)

    @classmethod
    async def retrieve_by_tag_filter(
        cls, storage: BaseStorage, tag_filter: dict
    ) -> "CredentialExchange":
        """Retrieve a credential exchange record by tag filter.

        Args:
            storage: The `BaseStorage` instance to use
            tag_filter: The filter dictionary to apply
        """
        result = await storage.search_records(
            cls.RECORD_TYPE, tag_filter
        ).fetch_single()
        vals = json.loads(result.value)
        vals.update(result.tags)
        return CredentialExchange(credential_exchange_id=result.id, **vals)

    @classmethod
    async def query(
        cls, storage: BaseStorage, tag_filter: dict = None
    ) -> Sequence["CredentialExchange"]:
        """Query existing credential exchange records.

        Args:
            storage: Storage implementation to use
            tag_filter: An optional dictionary of tag filter clauses
        """
        found = await storage.search_records(cls.RECORD_TYPE, tag_filter).fetch_all()
        result = []
        for record in found:
            vals = json.loads(record.value)
            vals.update(record.tags)
            result.append(CredentialExchange(credential_exchange_id=record.id, **vals))
        return result


class CredentialExchangeSchema(BaseModelSchema):
    """Schema to allow serialization/deserialization of credential exchange records."""

    class Meta:
        """CredentialExchangeSchema metadata."""

        model_class = CredentialExchange

    initiator = fields.Str(required=False)
    state = fields.Str(required=False)
    credential_definition_id = fields.Str(required=False)
    schema_id = fields.Str(required=False)
    credential_offer = fields.Dict(required=False)
    error_msg = fields.Str(required=False)
