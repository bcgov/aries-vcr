"""Record used to represent the form associated with an action menu option."""

from typing import Sequence

from marshmallow import fields

from ...models.base import BaseModel, BaseModelSchema

from .menu_form_param import MenuFormParam, MenuFormParamSchema


class MenuForm(BaseModel):
    """Instance of a form associated with an action menu item."""

    class Meta:
        """Menu form metadata."""

        schema_class = "MenuFormSchema"

    def __init__(
        self,
        *,
        title: str = None,
        description: str = None,
        params: Sequence[MenuFormParam] = None,
        submit_label: str = None,
    ):
        """
        Initialize a MenuForm instance.

        Args:
            title: The menu form title
            description: Additional descriptive text for the menu form
            params: A list of form parameters
            submit_label: An alternative label for the form submit button
        """
        self.title = title
        self.description = description
        self.params = list(params) if params else []
        self.submit_label = submit_label


class MenuFormSchema(BaseModelSchema):
    """MenuForm schema."""

    class Meta:
        """MenuFormSchema metadata."""

        model_class = MenuForm

    title = fields.Str(required=False)
    description = fields.Str(required=False)
    params = fields.List(fields.Nested(MenuFormParamSchema()), required=False)
    submit_label = fields.Str(data_key="submit-label", required=False)
