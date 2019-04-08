"""Indy implementation of BaseStorage interface."""

from typing import Mapping, Sequence

from indy.error import IndyError

from von_anchor.error import WalletState

from .base import BaseStorage, BaseStorageRecordSearch, StorageRecord
from .error import (
    StorageError,
    StorageDuplicateError,
    StorageNotFoundError,
    StorageSearchError,
)
from ..wallet.indyvon import IndyWallet


def _validate_record(record: StorageRecord):
    if not record:
        raise StorageError("No record provided")
    if not record.id:
        raise StorageError("Record has no ID")
    if not record.type:
        raise StorageError("Record has no type")
    if not StorageRecord.ok_tags(record.tags):
        raise StorageError("Non-trivial record tags must be flat str:str dict")


class IndyStorage(BaseStorage):
    """Indy Non-Secrets interface."""

    def __init__(self, wallet: IndyWallet):
        """
        Initialize a `BasicStorage` instance.

        Args:
            wallet: The indy wallet instance to use

        """
        self._wallet = wallet

    @property
    def wallet(self) -> IndyWallet:
        """Accessor for IndyWallet instance."""
        return self._wallet

    async def add_record(self, record: StorageRecord):
        """
        Add a new record to the store.

        Args:
            record: `StorageRecord` to be stored

        """
        _validate_record(record)
        if await self._wallet.get_non_secret(record.type, record.id):
            raise StorageDuplicateError("Duplicate record ID: {}".format(record.id))

        try:
            await self._wallet.write_non_secret(record)
        except WalletState as x_von:
            raise StorageError(str(x_von))
        except IndyError as x_indy:
            raise StorageError(str(x_indy))


    async def get_record(self, record_type: str, record_id: str) -> StorageRecord:
        """
        Fetch a record from the store by type and ID.

        Args:
            record_type: The record type
            record_id: The record id

        Returns:
            A `StorageRecord` instance

        Raises:
            StorageError: If the record is not provided
            StorageError: If the record ID not provided
            StorageNotFoundError: If the record is not found
            StorageError: If record not found

        """
        if not record_type:
            raise StorageError("Record type not provided")
        if not record_id:
            raise StorageError("Record ID not provided")

        try:
            found = await self._von_wallet.get_non_secret(record_type, record_id)
            if not found:
                raise StorageNotFoundError("Record not found: {}".format(record_id))
        except WalletState as x_von:
            raise StorageError(str(x_von))
        except IndyError as x_indy:
            raise StorageError(str(x_indy))
        return found[record_id]

    async def update_record_value(self, record: StorageRecord, value: str):
        """
        Update an existing stored record's value.

        Args:
            record: `StorageRecord` to update
            value: The new value

        Raises:
            StorageNotFoundError: If record not found
            StorageError: If a libindy error occurs

        """
        _validate_record(record)

        try:
            found = await self._von_wallet.get_non_secret(record.type, record.id)
            if not found:
                raise StorageNotFoundError("Record (type {}) not found: {}".format(record.type, record.id))
            non_secret = found[record.id]
            non_secret.value = record.value
            non_secret.tags = None
            await self._von_wallet.write_non_secret(non_secret, replace_meta=False)
        except WalletState as x_von:
            raise StorageError(str(x_von))
        except IndyError as x_indy:
            raise StorageError(str(x_indy))

    async def update_record_tags(self, record: StorageRecord, tags: Mapping):
        """
        Update an existing stored record's tags.

        Args:
            record: `StorageRecord` to update, by type and identifier
            tags: New tags, to augment existing tags (or replace on existing keys)

        Raises:
            StorageNotFoundError: If record not found
            StorageError: If a libindy error occurs

        """
        _validate_record(record)

        try:
            found = await self._von_wallet.get_non_secret(record.type, record.id)
            if not found:
                raise StorageNotFoundError("Record (type {}) not found: {}".format(record.type, record.id))
            non_secret = found[record.id]
            non_secret.tags = tags
            await self._von_wallet.write_non_secret(non_secret, replace_meta=False)
        except WalletState as x_von:
            raise StorageError(str(x_von))
        except IndyError as x_indy:
            raise StorageError(str(x_indy))

    async def delete_record_tags(
        self, record: StorageRecord, tags: (Sequence, Mapping)
    ):
        """
        Update an existing stored record's tags.

        Args:
            record: `StorageRecord` whose tags to delete, by type and identifier (implementation ignores its value)
            tags: Tags

        """
        _validate_record(record)

        try:
            found = await self._von_wallet.get_non_secret(record.type, record.id)
            if not found:
                raise StorageNotFoundError("Record (type {}) not found: {}".format(record.type, record.id))
            non_secret = found[record.id]
            non_secret.tags = None
            await self._von_wallet.write_non_secret(non_secret, replace_meta=True)
        except WalletState as x_von:
            raise StorageError(str(x_von))
        except IndyError as x_indy:
            raise StorageError(str(x_indy))

    async def delete_record(self, record: StorageRecord):
        """
        Delete a record.

        Args:
            record: `StorageRecord` to delete, by type and identifier

        Raises:
            StorageNotFoundError: If record not found
            StorageError: If a libindy error occurs

        """
        _validate_record(record)

        try:
            if not await self._von_wallet.get_non_secret(record.type, record.id):
                raise StorageNotFoundError("Record (type {}) not found: {}".format(record.type, record.id))
            await self._von_wallet.delete_non_secret(record.type, record.id)
        except WalletState as x_von:
            raise StorageError(str(x_von))
        except IndyError as x_indy:
            raise StorageError(str(x_indy))

    def search_records(
        self, type_filter: str, tag_query: Mapping = None, page_size: int = None
    ) -> "IndyStorageRecordSearch":
        """
        Search stored records.

        Args:
            type_filter: Filter string
            tag_query: Tags to query
            page_size: Page size

        Returns:
            An instance of `BaseStorageRecordSearch`

        """

        return IndyStorageRecordSearch(self, type_filter, tag_query, page_size)


class IndyStorageRecordSearch(BaseStorageRecordSearch):
    """Represent an active stored records search."""

    def __init__(
        self,
        store: IndyStorage,
        type_filter: str,
        tag_query: Mapping,
        page_size: int = None,
    ):
        """
        Initialize a `IndyStorageRecordSearch` instance.

        Args:
            store: `BaseStorage` to search
            type_filter: Filter string
            tag_query: Tags to search
            page_size: Size of page to return

        """
        super(IndyStorageRecordSearch, self).__init__(
            store, type_filter, tag_query, page_size
        )
        self._handle = None
        self._results = None
        self._cursor = 0

    @property
    def opened(self) -> bool:
        """
        Accessor for open state.

        Returns:
            True if opened, else False

        """
        return self._handle is not None

    @property
    def handle(self):
        """
        Accessor for search handle.

        Returns:
            The handle

        """
        return self._handle

    async def fetch(self, max_count: int) -> Sequence[StorageRecord]:
        """
        Fetch the next list of results from the store.

        Args:
            max_count: Max number of records to return

        Returns:
            A list of `StorageRecord`s

        Raises:
            StorageSearchError: If the search query has not been opened

        """
        if not self.opened:
            raise StorageSearchError("Search query has not been opened")
        last = self._cursor + min(max_count, len(self._result) - self._cursor)
        ret = self._result[self._cursor:last]
        self._cursor = last
        return ret

    async def open(self):
        """Start the search query."""
        try:
            self._results = []
            for storec in (await self.store.wallet.get_non_secret(self.type_filter, self.tag_query)).values():
                self._results.append(storec)
            self._cursor = 0
        except WalletState as x_von:
            raise StorageError(str(x_von))
        except IndyError as x_indy:
            raise StorageError(str(x_indy))
        self._handle = 1

    async def close(self):
        """Dispose of the search query."""
        self._handle = None
        self._cursor = 0
