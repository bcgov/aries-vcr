from unittest import mock, TestCase

from ..menu import Menu, MenuSchema
from ...models.menu_form import MenuForm
from ...models.menu_form_param import MenuFormParam
from ...models.menu_option import MenuOption
from ...message_types import MENU


class TestConfig:
    test_menu_message = {
        "title": "Welcome to IIWBook",
        "description": "IIWBook facilitates connections between attendees by verifying attendance and distributing connection invitations.",
        "options": [
            MenuOption(
                **{
                    "name": "search-introductions",
                    "title": "Search introductions",
                    "description": "Your email address must be verified to perform a search",
                    "disabled": True,
                    "form": MenuForm(
                        **{
                            "title": "Search introductions",
                            "description": "Enter a participant name below to perform a search.",
                            "params": [
                                MenuFormParam(
                                    **{
                                        "name": "query",
                                        "title": "Participant name",
                                        "default": "",
                                        "description": "",
                                        "required": True,
                                        "input_type": "text",
                                    }
                                )
                            ],
                            "submit_label": "Search",
                        }
                    ),
                }
            )
        ],
    }


class TestMenu(TestCase, TestConfig):
    def setUp(self):
        self.menu = Menu(**self.test_menu_message)

    def test_init(self):
        """Test initialization."""
        assert self.menu.title == self.test_menu_message["title"]
        assert self.menu.description == self.test_menu_message["description"]
        assert len(self.menu.options) == len(self.test_menu_message["options"])

    def test_type(self):
        """Test type."""
        assert self.menu._type == MENU

    @mock.patch(
        "indy_catalyst_agent.messaging.actionmenu.messages.menu.MenuSchema.load"
    )
    def test_deserialize(self, mock_menu_schema_load):
        """
        Test deserialization.
        """
        obj = {"obj": "obj"}

        menu = Menu.deserialize(obj)
        mock_menu_schema_load.assert_called_once_with(obj)

        assert menu is mock_menu_schema_load.return_value

    @mock.patch(
        "indy_catalyst_agent.messaging.actionmenu.messages.menu.MenuSchema.dump"
    )
    def test_serialize(self, mock_menu_schema_dump):
        """
        Test serialization.
        """
        menu_dict = self.menu.serialize()
        mock_menu_schema_dump.assert_called_once_with(self.menu)
        assert menu_dict is mock_menu_schema_dump.return_value

    def test_make_model(self):
        data = self.menu.serialize()
        model_instance = Menu.deserialize(data)
        assert type(model_instance) is type(self.menu)
