"""Base classes for Models and Schemas."""

from abc import ABC
import json
from typing import Union

from marshmallow import Schema, post_dump, pre_load, post_load, ValidationError

from ...classloader import ClassLoader
from ...error import BaseError


def resolve_class(the_cls, relative_cls: type = None):
    """
    Resolve a class.

    Args:
        the_cls: The class to resolve
        relative_cls: Relative class to resolve from

    Returns:
        The resolved class

    Raises:
        ClassNotFoundError: If the class could not be loaded

    """
    resolved = None
    if isinstance(the_cls, type):
        resolved = the_cls
    elif isinstance(the_cls, str):
        default_module = relative_cls and relative_cls.__module__
        resolved = ClassLoader.load_class(the_cls, default_module)
    return resolved


def resolve_meta_property(obj, prop_name: str, defval=None):
    """
    Resolve a meta property.

    Args:
        prop_name: The property to resolve
        defval: The default value

    Returns:
        The meta property

    """
    cls = obj.__class__
    found = defval
    while cls:
        Meta = getattr(cls, "Meta", None)
        if Meta and hasattr(Meta, prop_name):
            found = getattr(Meta, prop_name)
            break
        cls = cls.__bases__[0]
        if cls is object:
            break
    return found


class BaseModelError(BaseError):
    """Base exception class for base model errors."""


class BaseModel(ABC):
    """Base model that provides convenience methods."""

    class Meta:
        """BaseModel meta data."""

        schema_class = None

    def __init__(self):
        """
        Initialize BaseModel.

        Raises:
            TypeError: If schema_class is not set on Meta

        """
        if not self.Meta.schema_class:
            raise TypeError(
                "Can't instantiate abstract class {} with no schema_class".format(
                    self.__class__.__name__
                )
            )

    @classmethod
    def _get_schema_class(cls):
        """
        Get the schema class.

        Returns:
            The resolved schema class

        """
        return resolve_class(cls.Meta.schema_class, cls)

    @property
    def Schema(self) -> type:
        """
        Accessor for the model's schema class.

        Returns:
            The schema class

        """
        return self._get_schema_class()

    @classmethod
    def deserialize(cls, obj):
        """
        Convert from JSON representation to a model instance.

        Args:
            obj: The dict to load into a model instance

        Returns:
            A model instance for this data

        """
        schema = cls._get_schema_class()()
        try:
            return schema.loads(obj) if isinstance(obj, str) else schema.load(obj)
        except ValidationError as e:
            raise BaseModelError("Schema validation failed") from e

    def serialize(self, as_string=False) -> dict:
        """
        Create a JSON-compatible dict representation of the model instance.

        Args:
            as_string: Return a string of JSON instead of a dict

        Returns:
            A dict representation of this model, or a JSON string if as_string is True

        """
        schema = self.Schema()
        try:
            return schema.dumps(self) if as_string else schema.dump(self)
        except ValidationError as e:
            raise BaseModelError("Schema validation failed") from e

    @classmethod
    def from_json(cls, json_repr: Union[str, bytes]):
        """
        Parse a JSON string into a model instance.

        Args:
            json_repr: JSON string

        Returns:
            A model instance representation of this JSON

        """
        try:
            parsed = json.loads(json_repr)
        except ValueError as e:
            raise BaseModelError("JSON parsing failed") from e
        return cls.deserialize(parsed)

    def to_json(self) -> str:
        """
        Create a JSON representation of the model instance.

        Returns:
            A JSON representation of this message

        """
        return json.dumps(self.serialize())

    def __repr__(self) -> str:
        """
        Return a human readable representation of this class.

        Returns:
            A human readable string for this class

        """
        exclude = resolve_meta_property(self, "repr_exclude", [])
        items = (
            "{}={}".format(k, repr(v))
            for k, v in self.__dict__.items()
            if k not in exclude
        )
        return "<{}({})>".format(self.__class__.__name__, ", ".join(items))


class BaseModelSchema(Schema):
    """BaseModel schema."""

    class Meta:
        """BaseModelSchema metadata."""

        model_class = None
        skip_values = [None]
        ordered = True

    def __init__(self, *args, **kwargs):
        """
        Initialize BaseModelSchema.

        Raises:
            TypeError: If model_class is not set on Meta

        """
        super(BaseModelSchema, self).__init__(*args, **kwargs)
        if not self.Meta.model_class:
            raise TypeError(
                "Can't instantiate abstract class {} with no model_class".format(
                    self.__class__.__name__
                )
            )

    @classmethod
    def _get_model_class(cls):
        """
        Get the model class.

        Returns:
            The model class

        """
        return resolve_class(cls.Meta.model_class, cls)

    @property
    def Model(self) -> type:
        """
        Accessor for the schema's model class.

        Returns:
            The model class

        """
        return self._get_model_class()

    @pre_load
    def skip_dump_only(self, data):
        """
        Skip fields that are only expected during serialization.

        Args:
            data: The incoming data to clean

        Returns:
            The modified data

        """
        # not sure why this is necessary, seems like a bug
        to_remove = {
            field_obj.data_key or field_name
            for field_name, field_obj in self.fields.items()
            if field_obj.dump_only
        }
        for field_name in to_remove:
            if field_name in data:
                del data[field_name]
        return data

    @post_load
    def make_model(self, data: dict):
        """
        Return model instance after loading.

        Returns:
            A model instance

        """
        return self.Model(**data)

    @post_dump
    def remove_skipped_values(self, data):
        """
        Remove values that are are marked to skip.

        Returns:
            Returns this modified data

        """
        skip_vals = resolve_meta_property(self, "skip_values", [])
        return {key: value for key, value in data.items() if value not in skip_vals}
