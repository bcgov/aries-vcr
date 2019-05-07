"""Indy implementation of BaseWallet interface."""

import json
from typing import Sequence

from von_anchor.error import (
    BadAccess,
    AbsentMessage,
    AbsentRecord,
    AbsentWallet,
    ExtantRecord,
    ExtantWallet,
    VonAnchorError,
    WalletState,
)
from von_anchor.wallet import WalletManager

from indy.error import IndyError, ErrorCode

from .base import BaseWallet, KeyInfo, DIDInfo, PairwiseInfo
from .crypto import random_seed, validate_seed
from .error import WalletError, WalletDuplicateError, WalletNotFoundError
from .util import bytes_to_b64


class IndyWallet(BaseWallet):
    """Indy wallet implementation."""

    DEFAULT_KEY = ""
    DEFAULT_NAME = "default"
    W_MGR = WalletManager(
        {"storage_type": None, "freshness_time": 0, "key": DEFAULT_KEY}
    )

    def __init__(self, config: dict = None):
        """
        Initialize a `IndyWallet` instance.

        Args:
            config: {name, key, seed, did, auto_create, auto_remove}

        """
        if not config:
            config = {}
        super(IndyWallet, self).__init__(config)

        self._master_secret_id = None
        self._von_wallet = IndyWallet.W_MGR.get(
            config={
                **config,
                "name": config.get("name", config.get("id", IndyWallet.DEFAULT_NAME)),
            },
            access=config.get("key", IndyWallet.DEFAULT_KEY),
        )

    @property
    def handle(self):
        """
        Get internal wallet reference.

        Returns:
            A handle to the wallet

        """
        return self.von_wallet.handle

    @property
    def opened(self) -> bool:
        """
        Check whether wallet is currently open.

        Returns:
            True if open, else False

        """
        return self.von_wallet.opened

    @property
    def master_secret_id(self) -> str:
        """Accessor for the linked secret label."""
        return self._master_secret_id

    @property
    def name(self) -> str:
        """
        Accessor for the wallet name.

        Returns:
            The wallet name

        """
        return self.von_wallet.name

    @property
    def von_wallet(self):
        """
        Get internal VON anchor wallet reference.

        Returns:
            A VON anchor wallet reference

        """
        return self._von_wallet

    async def create(self, replace: bool = False):
        """
        Create a new wallet.

        Args:
            replace: Removes the old wallet if True

        Raises:
            WalletError: If there was a problem removing the wallet
            WalletError: IF there was a libindy error

        """
        try:
            await IndyWallet.W_MGR.create(
                self.von_wallet.config, access=self.von_wallet.access, replace=replace
            )
        except ExtantWallet:
            raise WalletError(
                "Wallet was not removed by SDK, may still be open: {}".format(self.name)
            )
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

    async def remove(self):
        """
        Remove an existing wallet.

        Raises:
            WalletNotFoundError: If the wallet could not be found
            WalletError: If there was an libindy error

        """
        try:
            await IndyWallet.W_MGR.remove(self.von_wallet)
        except WalletState as x_von:
            raise WalletError(str(x_von))
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.WalletNotFoundError:
                raise WalletNotFoundError("Wallet not found: {}".format(self.name))
            raise WalletError(str(x_indy))

    async def open(self):
        """
        Open wallet, removing and/or creating it if so configured.

        Raises:
            WalletError: If wallet not found after creation
            WalletError: On bad access credentials value
            WalletNotFoundError: If the wallet is not found
            WalletError: If the wallet is already open
            WalletError: If there is a libindy error

        """
        try:
            await self.von_wallet.open()
        except AbsentWallet:
            raise WalletError("Wallet not found after creation: {}".format(self.name))
        except WalletState:
            raise WalletError("Wallet is already open: {}".format(self.name))
        except BadAccess:
            raise WalletError(
                "Cannot open wallet {}: bad access credentials value".format(self.name)
            )
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

        self._master_secret_id = await self.von_wallet.get_link_secret_label()

    async def close(self):
        """Close previously-opened wallet, removing it if so configured."""
        await self.von_wallet.close()

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
        try:
            return await self.von_wallet.create_signing_key(
                bytes_to_b64(validate_seed(seed) if seed else random_seed()),
                metadata=metadata,
            )
        except ExtantRecord:
            raise WalletDuplicateError(
                "Verification key already present in wallet {}".format(self.name)
            )
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

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
            return await self.von_wallet.get_signing_key(verkey)
        except AbsentRecord:
            raise WalletNotFoundError(
                "Wallet {} has no signing key pair for verkey {}".format(
                    self.name, verkey
                )
            )
        except VonAnchorError as x_von:
            raise WalletError(str(x_von))
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

    async def replace_signing_key_metadata(self, verkey: str, metadata: dict):
        """
        Replace the metadata associated with a signing keypair.

        Args:
            verkey: The verification key of the keypair
            metadata: The new metadata to store

        Raises:
            WalletNotFoundError: if no keypair is associated with the verification key

        """
        try:
            await self.von_wallet.replace_signing_key_metadata(verkey, metadata)
        except AbsentRecord:
            raise WalletNotFoundError(
                "Wallet {} has no signing key pair for verkey {}".format(
                    self.name, verkey
                )
            )
        except VonAnchorError as x_von:
            raise WalletError(str(x_von))
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

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
        try:
            return await self.von_wallet.create_local_did(
                bytes_to_b64(validate_seed(seed) if seed else random_seed()),
                did,
                metadata,
            )
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except ExtantRecord:
            raise WalletDuplicateError("DID already present in wallet")
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

    async def get_local_dids(self) -> Sequence[DIDInfo]:
        """
        Get list of defined local DIDs.

        Returns:
            A list of locally stored DIDs as `DIDInfo` instances

        """
        return await self.von_wallet.get_local_dids()

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
            return await self.von_wallet.get_local_did(did)
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except AbsentRecord:
            raise WalletNotFoundError(
                "Wallet {} has no signing key pair DID {}".format(self.name, did)
            )
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

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

        try:
            return await self.von_wallet.get_local_did(verkey)
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except AbsentRecord:
            raise WalletNotFoundError(
                "Wallet {} has no signing key pair for verkey {}".format(
                    self.name, verkey
                )
            )
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

    async def replace_local_did_metadata(self, did: str, metadata: dict):
        """
        Replace metadata for a local DID.

        Args:
            did: The DID to replace metadata for
            metadata: The new metadata

        Raises:
            WalletNotFoundError: If the local DID is not present

        """
        try:
            await self.von_wallet.replace_local_did_metadata(did, metadata)
        except AbsentRecord:
            raise WalletNotFoundError(
                "Wallet {} has no local DID {}".format(self.name, did)
            )

    async def create_pairwise(
        self,
        their_did: str,
        their_verkey: str,
        my_did: str = None,
        metadata: dict = None,
    ) -> PairwiseInfo:
        """
        Create pairwise DID for a secure connection.

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

        if their_did in await self.von_wallet.get_pairwise(their_did):
            raise WalletDuplicateError(
                "Pairwise DID for {} already present in wallet {}".format(
                    their_did, self.name
                )
            )

        try:
            return await self.von_wallet.write_pairwise(
                their_did, their_verkey, my_did, metadata, replace_meta=True
            )
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

    async def get_pairwise_list(self) -> Sequence[PairwiseInfo]:
        """
        Get list of defined pairwise DIDs.

        Returns:
            A list of `PairwiseInfo` instances for all pairwise relationships

        """
        return [pwinfo for pwinfo in (await self.von_wallet.get_pairwise()).values()]

    async def get_pairwise_for_did(self, their_did: str) -> PairwiseInfo:
        """
        Find info for a pairwise DID.

        Args:
            their_did: The DID to get a pairwise relationship for

        Returns:
            A `PairwiseInfo` instance representing the relationship

        Raises:
            WalletNotFoundError: If no pairwise DID defined for target

        """
        found = await self.von_wallet.get_pairwise(their_did)
        if not found:
            raise WalletNotFoundError(
                "No pairwise DID defined for target: {}".format(their_did)
            )
        return found[their_did]

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
        found = await self.von_wallet.get_pairwise(
            json.dumps({"their_verkey": their_verkey})
        )
        if not found:
            raise WalletNotFoundError(
                "No pairwise DID defined for target: {}".format(their_verkey)
            )
        return [pwise for pwise in found.values()][0]

    async def replace_pairwise_metadata(self, their_did: str, metadata: dict):
        """
        Replace metadata for a pairwise DID.

        Args:
            their_did: The DID to replace metadata for
            metadata: The new metadata

        Raises:
            WalletNotFoundError: If no pairwise DID is defined for target

        """
        try:
            await self.von_wallet.write_pairwise(
                their_did, metadata=metadata, replace_meta=True
            )
        except AbsentRecord:
            raise WalletNotFoundError(
                "No pairwise DID defined for target: {}".format(their_did)
            )

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
        if not from_verkey:
            raise WalletError("Verkey not provided")

        try:
            result = await self.von_wallet.sign(message, from_verkey)
        except AbsentMessage:
            raise WalletError("Message not provided")
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

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

        try:
            result = await self.von_wallet.verify(message, signature, from_verkey)
        except AbsentMessage:
            raise WalletError("Message not provided")
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except IndyError as x_indy:
            if x_indy.error_code == ErrorCode.CommonInvalidStructure:  # how to get?
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
            WalletError: If message is absent
            WalletError: If verification key is not specified
            WalletError: If wallet is closed
            WalletError: If a libindy error occurs

        """
        if not to_verkey:
            raise WalletError("Recipient verkey not provided")

        try:
            return await self.von_wallet.encrypt(
                message,
                authn=bool(from_verkey),
                to_verkey=to_verkey,
                from_verkey=from_verkey,
            )
        except AbsentMessage:
            raise WalletError("Message not provided")
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

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
            WalletError: If ciphertext not provided

        """
        try:
            return await self.von_wallet.decrypt(
                ciphertext=enc_message,
                authn_check=False if use_auth else None,
                to_verkey=to_verkey,
                from_verkey=None,
            )
        except AbsentMessage:
            raise WalletError("Ciphertext not provided")
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

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
        try:
            return await self.von_wallet.pack(message, to_verkeys, from_verkey)
        except AbsentMessage:
            raise WalletError("Message not provided")
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except IndyError as x_indy:
            raise WalletError(str(x_indy))

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
        try:
            return await self.von_wallet.unpack(enc_message)
        except AbsentMessage:
            raise WalletError("Message not provided")
        except WalletState:
            raise WalletError("Wallet {} is closed".format(self.name))
        except AbsentRecord:
            raise WalletError("Ciphertext requires private key not in wallet {}")
        except IndyError as x_indy:
            raise WalletError(str(x_indy))
