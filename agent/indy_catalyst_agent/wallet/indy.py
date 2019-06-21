"""Indy implementation of BaseWallet interface."""

import json
import logging
from typing import Sequence

import indy.anoncreds
import indy.did
import indy.crypto
import indy.pairwise
from indy.error import IndyError, ErrorCode

from .base import BaseWallet, KeyInfo, DIDInfo, PairwiseInfo
from .crypto import validate_seed
from .error import WalletError, WalletDuplicateError, WalletNotFoundError
from .util import bytes_to_b64


class IndyWallet(BaseWallet):
    """Indy wallet implementation."""

    DEFAULT_FRESHNESS = 0
    DEFAULT_KEY = ""
    DEFAULT_NAME = "default"
    DEFAULT_STORAGE_TYPE = None

    def __init__(self, config: dict = None):
        """
        Initialize a `IndyWallet` instance.

        Args:
            config: {name, key, seed, did, auto-create, auto-remove,
                     storage_type, storage_config, storage_creds}

        """
        self.logger = logging.getLogger(__name__)

        if not config:
            config = {}
        super(IndyWallet, self).__init__(config)
        self._auto_create = config.get("auto_create", True)
        self._auto_remove = config.get("auto_remove", False)
        self._freshness_time = config.get("freshness_time", False)
        self._handle = None
        self._key = config.get("key") or self.DEFAULT_KEY
        self._name = config.get("name") or self.DEFAULT_NAME
        self._storage_type = config.get("storage_type") or self.DEFAULT_STORAGE_TYPE
        self._storage_config = config.get("storage_config", None)
        self._storage_creds = config.get("storage_creds", None)
        self._master_secret_id = None

    @property
    def handle(self):
        """
        Get internal wallet reference.

        Returns:
            A handle to the wallet

        """
        return self._handle

    @property
    def opened(self) -> bool:
        """
        Check whether wallet is currently open.

        Returns:
            True if open, else False

        """
        return bool(self._handle)

    @property
    def name(self) -> str:
        """
        Accessor for the wallet name.

        Returns:
            The wallet name

        """
        return self._name

    @property
    def master_secret_id(self) -> str:
        """
        Accessor for the master secret id.

        Returns:
            The master secret id

        """
        return self._master_secret_id

    @property
    def _wallet_config(self) -> dict:
        """
        Accessor for the wallet config.

        Returns:
            The wallet config

        """
        ret = {
            "id": self._name,
            "freshness_time": self._freshness_time,
            "storage_type": self._storage_type,
            # storage_config
        }
        if self._storage_config is not None:
            ret["storage_config"] = json.loads(self._storage_config)
        return ret

    @property
    def _wallet_access(self) -> dict:
        """
        Accessor for the wallet access.

        Returns:
            The wallet access

        """
        ret = {
            "key": self._key,
            # key_derivation_method
            # storage_credentials
        }
        if self._storage_creds is not None:
            ret["storage_credentials"] = json.loads(self._storage_creds)
        return ret

    async def create(self, replace: bool = False):
        """
        Create a new wallet.

        Args:
            replace: Removes the old wallet if True

        Raises:
            WalletError: If there was a problem removing the wallet
            WalletError: IF there was a libindy error

        """
        if replace:
            try:
                await self.remove()
            except WalletNotFoundError:
                pass
        try:
            await indy.wallet.create_wallet(
                config=json.dumps(self._wallet_config),
                credentials=json.dumps(self._wallet_access),
            )
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletAlreadyExistsError:
                raise WalletError(
                    "Wallet was not removed by SDK, may still be open: {}".format(
                        self.name
                    )
                )
            else:
                raise WalletError(str(x_indy))

    async def remove(self):
        """
        Remove an existing wallet.

        Raises:
            WalletNotFoundError: If the wallet could not be found
            WalletError: If there was an libindy error

        """
        try:
            await indy.wallet.delete_wallet(
                config=json.dumps(self._wallet_config),
                credentials=json.dumps(self._wallet_access),
            )
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletNotFoundError:
                raise WalletNotFoundError("Wallet not found: {}".format(self.name))
            raise WalletError(str(x_indy))

    async def open(self):
        """
        Open wallet, removing and/or creating it if so configured.

        Raises:
            WalletError: If wallet not found after creation
            WalletNotFoundError: If the wallet is not found
            WalletError: If the wallet is already open
            WalletError: If there is a libindy error

        """
        if self.opened:
            return

        created = False
        while True:
            try:
                self._handle = await indy.wallet.open_wallet(
                    config=json.dumps(self._wallet_config),
                    credentials=json.dumps(self._wallet_access),
                )
                break
            except IndyError as x_indy:
                if x_indy.error_code == ErrorCode.WalletNotFoundError:
                    if created:
                        raise WalletError(
                            "Wallet not found after creation: {}".format(self.name)
                        )
                    if self._auto_create:
                        await self.create(self._auto_remove)
                    else:
                        raise WalletNotFoundError(
                            "Wallet not found: {}".format(self.name)
                        )
                elif x_indy.error_code == ErrorCode.WalletAlreadyOpenedError:
                    raise WalletError("Wallet is already open: {}".format(self.name))
                else:
                    raise WalletError(str(x_indy))

        self.logger.info("Creating master secret...")
        try:
            self._master_secret_id = await indy.anoncreds.prover_create_master_secret(
                self.handle, self.name
            )
        except IndyError as error:
            if error.error_code == ErrorCode.AnoncredsMasterSecretDuplicateNameError:
                self.logger.info("Master secret already exists")
                self._master_secret_id = self.name
            else:
                raise

    async def close(self):
        """Close previously-opened wallet, removing it if so configured."""
        if self._handle:
            await indy.wallet.close_wallet(self._handle)
            if self._auto_remove:
                await self.remove()
            self._handle = None

    async def create_signing_key(
        self, seed: str = None, metadata: dict = None
    ) -> KeyInfo:
        """
        Create a new public/private signing keypair.

        Args:
            seed: Seed for key
            metadata: Optional metadata to store with the keypair

        Returns:
            A `KeyInfo` representing the new record

        Raises:
            WalletDuplicateError: If the resulting verkey already exists in the wallet
            WalletError: If there is a libindy error

        """
        args = {}
        if seed:
            args["seed"] = bytes_to_b64(validate_seed(seed))
        try:
            verkey = await indy.crypto.create_key(self.handle, json.dumps(args))
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletItemAlreadyExists:
                raise WalletDuplicateError("Verification key already present in wallet")
            else:
                raise WalletError(str(x_indy))
        # must save metadata to allow identity check
        # otherwise get_key_metadata just returns WalletItemNotFound
        if metadata is None:
            metadata = {}
        await indy.crypto.set_key_metadata(self.handle, verkey, json.dumps(metadata))
        return KeyInfo(verkey, metadata)

    async def get_signing_key(self, verkey: str) -> KeyInfo:
        """
        Fetch info for a signing keypair.

        Args:
            verkey: The verification key of the keypair

        Returns:
            A `KeyInfo` representing the keypair

        Raises:
            WalletNotFoundError: If no keypair is associated with the verification key
            WalletError: If there is a libindy error

        """
        try:
            metadata = await indy.crypto.get_key_metadata(self.handle, verkey)
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletItemNotFound:
                raise WalletNotFoundError("Unknown key: {}".format(verkey))
            else:
                raise WalletError(str(x_indy))
        return KeyInfo(verkey, json.loads(metadata) if metadata else {})

    async def replace_signing_key_metadata(self, verkey: str, metadata: dict):
        """
        Replace the metadata associated with a signing keypair.

        Args:
            verkey: The verification key of the keypair
            metadata: The new metadata to store

        Raises:
            WalletNotFoundError: if no keypair is associated with the verification key

        """
        meta_json = json.dumps(metadata or {})
        await self.get_signing_key(verkey)  # throw exception if key is undefined
        await indy.crypto.set_key_metadata(self.handle, verkey, meta_json)

    async def create_local_did(
        self, seed: str = None, did: str = None, metadata: dict = None
    ) -> DIDInfo:
        """
        Create and store a new local DID.

        Args:
            seed: Optional seed to use for did
            did: The DID to use
            metadata: Metadata to store with DID

        Returns:
            A `DIDInfo` instance representing the created DID

        Raises:
            WalletDuplicateError: If the DID already exists in the wallet
            WalletError: If there is a libindy error

        """
        cfg = {}
        if seed:
            cfg["seed"] = bytes_to_b64(validate_seed(seed))
        if did:
            cfg["did"] = did
        did_json = json.dumps(cfg)
        # crypto_type, cid - optional parameters skipped
        try:
            did, verkey = await indy.did.create_and_store_my_did(self.handle, did_json)
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.DidAlreadyExistsError:
                raise WalletDuplicateError("DID already present in wallet")
            else:
                raise WalletError(str(x_indy))
        if metadata:
            await self.replace_local_did_metadata(did, metadata)
        return DIDInfo(did, verkey, metadata)

    async def get_local_dids(self) -> Sequence[DIDInfo]:
        """
        Get list of defined local DIDs.

        Returns:
            A list of locally stored DIDs as `DIDInfo` instances

        """
        info_json = await indy.did.list_my_dids_with_meta(self.handle)
        info = json.loads(info_json)
        ret = []
        for did in info:
            ret.append(
                DIDInfo(
                    did=did["did"],
                    verkey=did["verkey"],
                    metadata=json.loads(did["metadata"]) if did["metadata"] else {},
                )
            )
        return ret

    async def get_local_did(self, did: str) -> DIDInfo:
        """
        Find info for a local DID.

        Args:
            did: The DID to get info for

        Returns:
            A `DIDInfo` instance representing the found DID

        Raises:
            WalletNotFoundError: If the DID is not found
            WalletError: If there is a libindy error

        """

        try:
            info_json = await indy.did.get_my_did_with_meta(self.handle, did)
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletItemNotFound:
                raise WalletNotFoundError("Unknown DID: {}".format(did))
            else:
                raise WalletError(str(x_indy))
        info = json.loads(info_json)
        return DIDInfo(
            did=info["did"],
            verkey=info["verkey"],
            metadata=json.loads(info["metadata"]) if info["metadata"] else {},
        )

    async def get_local_did_for_verkey(self, verkey: str) -> DIDInfo:
        """
        Resolve a local DID from a verkey.

        Args:
            verkey: The verkey to get the local DID for

        Returns:
            A `DIDInfo` instance representing the found DID

        Raises:
            WalletNotFoundError: If the verkey is not found

        """

        dids = await self.get_local_dids()
        for info in dids:
            if info.verkey == verkey:
                return info
        raise WalletNotFoundError("No DID defined for verkey: {}".format(verkey))

    async def replace_local_did_metadata(self, did: str, metadata: dict):
        """
        Replace metadata for a local DID.

        Args:
            did: The DID to replace metadata for
            metadata: The new metadata

        """
        meta_json = json.dumps(metadata or {})
        await self.get_local_did(did)  # throw exception if undefined
        await indy.did.set_did_metadata(self.handle, did, meta_json)

    async def create_pairwise(
        self,
        their_did: str,
        their_verkey: str,
        my_did: str = None,
        metadata: dict = None,
    ) -> PairwiseInfo:
        """
        Create a new pairwise DID for a secure connection.

        Args:
            their_did: The other party's DID
            their_verkey: The other party's verkey
            my_did: My DID
            metadata: Metadata to store with this relationship

        Returns:
            A `PairwiseInfo` object representing the pairwise connection

        Raises:
            WalletError: If there is a libindy error
            WalletDuplicateError: If the DID already exists in the wallet

        """

        # store their DID info in wallet
        ident_json = json.dumps({"did": their_did, "verkey": their_verkey})
        try:
            await indy.did.store_their_did(self.handle, ident_json)
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletItemAlreadyExists:
                # their DID already stored, but real test is creating pairwise
                pass
            else:
                raise WalletError(str(x_indy))

        # create a new local DID for this pairwise connection
        if my_did:
            my_info = await self.get_local_did(my_did)
        else:
            my_info = await self.create_local_did(
                None, None, {"pairwise_for": their_did}
            )

        # create the pairwise record
        combined_meta = {
            # info that should be returned in pairwise_info struct but isn't
            "their_verkey": their_verkey,
            "my_verkey": my_info.verkey,
            "custom": metadata or {},
        }
        meta_json = json.dumps(combined_meta)
        try:
            await indy.pairwise.create_pairwise(
                self.handle, their_did, my_info.did, meta_json
            )
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletItemAlreadyExists:
                raise WalletDuplicateError(
                    "Pairwise DID already present in wallet: {}".format(their_did)
                )
            else:
                raise WalletError(str(x_indy))

        return PairwiseInfo(
            their_did=their_did,
            their_verkey=their_verkey,
            my_did=my_info.did,
            my_verkey=my_info.verkey,
            metadata=combined_meta["custom"],
        )

    def _make_pairwise_info(self, result: dict, their_did: str = None) -> PairwiseInfo:
        """
        Convert Indy pairwise info into PairwiseInfo record.

        Args:
            result:
            their_did

        Returns:
            A new `PairwiseInfo` instance

        """
        meta = result["metadata"] and json.loads(result["metadata"]) or {}
        if "custom" not in meta:
            # not one of our pairwise records
            return None
        return PairwiseInfo(
            their_did=result.get("their_did", their_did),
            their_verkey=meta.get("their_verkey"),
            my_did=result.get("my_did"),
            my_verkey=meta.get("my_verkey"),
            metadata=meta["custom"],
        )

    async def get_pairwise_list(self) -> Sequence[PairwiseInfo]:
        """
        Get list of defined pairwise DIDs.

        Returns:
            A list of `PairwiseInfo` instances for all pairwise relationships

        """
        pairs_json = await indy.pairwise.list_pairwise(self.handle)
        pairs = json.loads(pairs_json)
        ret = []
        for pair_json in pairs:
            pair = json.loads(pair_json)
            info = self._make_pairwise_info(pair)
            if info:
                ret.append(info)
        return ret

    async def get_pairwise_for_did(self, their_did: str) -> PairwiseInfo:
        """
        Find info for a pairwise DID.

        Args:
            their_did: The DID to get a pairwise relationship for

        Returns:
            A `PairwiseInfo` instance representing the relationship

        Raises:
            WalletNotFoundError: If no pairwise DID defined for target
            WalletNotFoundError: If no pairwise DID defined for target

        """
        try:
            pair_json = await indy.pairwise.get_pairwise(self.handle, their_did)
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletItemNotFound:
                raise WalletNotFoundError(
                    "No pairwise DID defined for target: {}".format(their_did)
                )
            else:
                raise WalletError(str(x_indy))
        pair = json.loads(pair_json)
        info = self._make_pairwise_info(pair, their_did)
        if not info:
            raise WalletNotFoundError(
                "No pairwise DID defined for target: {}".format(their_did)
            )
        return info

    async def get_pairwise_for_verkey(self, their_verkey: str) -> PairwiseInfo:
        """
        Resolve a pairwise DID from a verkey.

        Args:
            their_verkey: The verkey to get a pairwise relationship for

        Returns:
            A `PairwiseInfo` instance for the relationship

        Raises:
            WalletNotFoundError: If no pairwise DID is defined for verkey

        """
        dids = await self.get_pairwise_list()
        for info in dids:
            if info.their_verkey == their_verkey:
                return info
        raise WalletNotFoundError(
            "No pairwise DID defined for verkey: {}".format(their_verkey)
        )

    async def replace_pairwise_metadata(self, their_did: str, metadata: dict):
        """
        Replace metadata for a pairwise DID.

        Args:
            their_did: The DID to replace metadata for
            metadata: The new metadata

        """
        info = await self.get_pairwise_for_did(
            their_did
        )  # throws exception if undefined
        meta_upd = info.metadata.copy()
        meta_upd.update({"custom": metadata or {}})
        upd_json = json.dumps(meta_upd)
        await indy.pairwise.set_pairwise_metadata(self.handle, their_did, upd_json)

    async def sign_message(self, message: bytes, from_verkey: str) -> bytes:
        """
        Sign a message using the private key associated with a given verkey.

        Args:
            message: Message bytes to sign
            from_verkey: The verkey to use to sign

        Returns:
            A signature

        Raises:
            WalletError: If the message is not provided
            WalletError: If the verkey is not provided
            WalletError: If a libindy error occurs

        """
        if not message:
            raise WalletError("Message not provided")
        if not from_verkey:
            raise WalletError("Verkey not provided")
        try:
            result = await indy.crypto.crypto_sign(self.handle, from_verkey, message)
        except IndyError:
            raise WalletError("Exception when signing message")
        return result

    async def verify_message(
        self, message: bytes, signature: bytes, from_verkey: str
    ) -> bool:
        """
        Verify a signature against the public key of the signer.

        Args:
            message: Message to verify
            signature: Signature to verify
            from_verkey: Verkey to use in verification

        Returns:
            True if verified, else False

        Raises:
            WalletError: If the verkey is not provided
            WalletError: If the signature is not provided
            WalletError: If the message is not provided
            WalletError: If a libindy error occurs

        """
        if not from_verkey:
            raise WalletError("Verkey not provided")
        if not signature:
            raise WalletError("Signature not provided")
        if not message:
            raise WalletError("Message not provided")
        try:
            result = await indy.crypto.crypto_verify(from_verkey, message, signature)
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.CommonInvalidStructure:
                result = False
            else:
                raise WalletError(str(x_indy))
        return result

    async def encrypt_message(
        self, message: bytes, to_verkey: str, from_verkey: str = None
    ) -> bytes:
        """
        Apply auth_crypt or anon_crypt to a message.

        Args:
            message: The binary message content
            to_verkey: The verkey of the recipient
            from_verkey: The verkey of the sender. If provided then auth_crypt is used,
                otherwise anon_crypt is used.

        Returns:
            The encrypted message content

        Raises:
            WalletError: If a libindy error occurs

        """
        if from_verkey:
            try:
                result = await indy.crypto.auth_crypt(
                    self.handle, from_verkey, to_verkey, message
                )
            except IndyError:
                raise WalletError("Exception when encrypting auth message")
        else:
            try:
                result = await indy.crypto.anon_crypt(to_verkey, message)
            except IndyError:
                raise WalletError("Exception when encrypting anonymous message")
        return result

    async def decrypt_message(
        self, enc_message: bytes, to_verkey: str, use_auth: bool
    ) -> (bytes, str):
        """
        Decrypt a message assembled by auth_crypt or anon_crypt.

        Args:
            message: The encrypted message content
            to_verkey: The verkey of the recipient. If provided then auth_decrypt is
                used, otherwise anon_decrypt is used.
            use_auth: True if you would like to auth_decrypt, False for anon_decrypt

        Returns:
            A tuple of the decrypted message content and sender verkey
            (None for anon_crypt)

        Raises:
            WalletError: If a libindy error occurs

        """
        if use_auth:
            try:
                sender_verkey, result = await indy.crypto.auth_decrypt(
                    self.handle, to_verkey, enc_message
                )
            except IndyError:
                raise WalletError("Exception when decrypting auth message")
        else:
            try:
                result = await indy.crypto.anon_decrypt(
                    self.handle, to_verkey, enc_message
                )
            except IndyError:
                raise WalletError("Exception when decrypting anonymous message")
            sender_verkey = None
        return result, sender_verkey

    async def pack_message(
        self, message: str, to_verkeys: Sequence[str], from_verkey: str = None
    ) -> bytes:
        """
        Pack a message for one or more recipients.

        Args:
            message: The message to pack
            to_verkeys: List of verkeys to pack for
            from_verkey: Sender verkey to pack from

        Returns:
            The resulting packed message bytes

        Raises:
            WalletError: If no message is provided
            WalletError: If a libindy error occurs

        """
        if message is None:
            raise WalletError("Message not provided")
        try:
            result = await indy.crypto.pack_message(
                self.handle, message, to_verkeys, from_verkey
            )
        except IndyError:
            raise WalletError("Exception when packing message")
        return result

    async def unpack_message(self, enc_message: bytes) -> (str, str, str):
        """
        Unpack a message.

        Args:
            enc_message: The packed message bytes

        Returns:
            A tuple: (message, from_verkey, to_verkey)

        Raises:
            WalletError: If the message is not provided
            WalletError: If a libindy error occurs

        """
        if not enc_message:
            raise WalletError("Message not provided")
        try:
            unpacked_json = await indy.crypto.unpack_message(self.handle, enc_message)
        except IndyError:
            raise WalletError("Exception when unpacking message")
        unpacked = json.loads(unpacked_json)
        message = unpacked["message"]
        to_verkey = unpacked.get("recipient_verkey", None)
        from_verkey = unpacked.get("sender_verkey", None)
        return message, from_verkey, to_verkey
