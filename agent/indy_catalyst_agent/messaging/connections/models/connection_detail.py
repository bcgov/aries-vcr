"""An object for containing the connection request/response DID information."""

from marshmallow import fields

from von_anchor.a2a import DIDDoc

from ...models.base import BaseModel, BaseModelSchema


class DIDDocWrapper(fields.Field):
    """Field that loads and serializes DIDDoc."""

    def _serialize(self, value, attr, obj, **kwargs):
        """
        Serialize the DIDDoc.

        Args:
            value: The value to serialize

        Returns:
            The serialized DIDDoc

        """
        return value.serialize()

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Deserialize a value into a DIDDoc.

        Args:
            value: The value to deserialize

        Returns:
            The deserialized value

        """
        # quick fix for missing optional values
        if "authentication" not in value:
            value["authentication"] = []
        if "service" not in value:
            value["service"] = []
        return DIDDoc.deserialize(value)


class ConnectionDetail(BaseModel):
    """Class representing the details of a connection."""

    class Meta:
        """ConnectionDetail metadata."""

        schema_class = "ConnectionDetailSchema"

    def __init__(self, *, did: str = None, did_doc: DIDDoc = None, **kwargs):
        """
        Initialize a ConnectionDetail instance.

        Args:
            did: DID for the connection detail
            did_doc: DIDDoc for connection detail

        """
        super(ConnectionDetail, self).__init__(**kwargs)
        self._did = did
        self._did_doc = did_doc

    @property
    def did(self) -> str:
        """
        Accessor for the connection DID.

        Returns:
            The DID for this connection

        """
        return self._did

    @property
    def did_doc(self) -> DIDDoc:
        """
        Accessor for the connection DID Document.

        Returns:
            The DIDDoc for this connection

        """
        return self._did_doc


class ConnectionDetailSchema(BaseModelSchema):
    """ConnectionDetail schema."""

    class Meta:
        """ConnectionDetailSchema metadata."""

        model_class = "ConnectionDetail"

    did = fields.Str(data_key="DID", required=False)
    did_doc = DIDDocWrapper(data_key="DIDDoc", required=False)
