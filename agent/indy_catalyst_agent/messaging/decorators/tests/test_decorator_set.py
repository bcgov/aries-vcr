from marshmallow import fields
from unittest import TestCase

from ...models.base import BaseModel, BaseModelSchema

from ..base import BaseDecoratorSet


class SimpleModel(BaseModel):
    class Meta:
        schema_class = "SimpleModelSchema"

    def __init__(self, *, value: str = None, **kwargs):
        super().__init__(**kwargs)
        self.value = value


class SimpleModelSchema(BaseModelSchema):
    class Meta:
        model_class = SimpleModel

    value = fields.Str(required=True)


class TestDecoratorSet(TestCase):
    def test_extract(self):

        decor_value = {}
        message = {"~decorator": decor_value, "one": "TWO"}

        decors = BaseDecoratorSet()
        remain = decors.extract_decorators(message)

        # check original is unmodified
        assert "~decorator" in message

        assert decors["decorator"] is decor_value
        assert remain == {"one": "TWO"}

    def test_dict(self):

        decors = BaseDecoratorSet()
        decors["test"] = "TEST"
        assert decors["test"] == "TEST"
        result = decors.to_dict()
        assert result == {"~test": "TEST"}

    def test_decorator_model(self):

        decor_value = {}
        message = {"~test": {"value": "TEST"}}

        decors = BaseDecoratorSet()
        decors.add_model("test", SimpleModel)
        remain = decors.extract_decorators(message)

        tested = decors["test"]
        assert isinstance(tested, SimpleModel) and tested.value == "TEST"

        result = decors.to_dict()
        assert result == message

    def test_field_decorator(self):

        decor_value = {}
        message = {"test~decorator": decor_value, "one": "TWO"}

        decors = BaseDecoratorSet()
        remain = decors.extract_decorators(message)

        # check original is unmodified
        assert "test~decorator" in message

        assert decors.field("test")
        assert decors.field("test")["decorator"] is decor_value
        assert remain == {"one": "TWO"}
