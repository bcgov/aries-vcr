"""Record used to represent individual menu options in an action menu."""

from marshmallow import fields

from ...models.base import BaseModel, BaseModelSchema

from .menu_form import MenuForm, MenuFormSchema


class MenuOption(BaseModel):
    """Instance of a menu option associated with an action menu."""

    class Meta:
        """Menu option metadata."""

        schema_class = "MenuOptionSchema"

    def __init__(
        self,
        *,
        name: str = None,
        title: str = None,
        description: str = None,
        disabled: bool = None,
        form: MenuForm = None,
    ):
        """
        Initialize a MenuOption instance.

        Args:
            name: The menu option name (unique ID)
            title: The menu option title
            description: Additional descriptive text for the menu option
            disabled: If the option should be shown as disabled
            form: A form to display when the option is selected
        """
        self.name = name
        self.title = title
        self.description = description
        self.disabled = disabled
        self.form = form


class MenuOptionSchema(BaseModelSchema):
    """MenuOption schema."""

    class Meta:
        """MenuOptionSchema metadata."""

        model_class = MenuOption

    name = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    disabled = fields.Bool(required=False)
    form = fields.Nested(MenuFormSchema(), required=False)
