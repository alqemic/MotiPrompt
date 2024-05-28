import json
import unittest
from unittest.mock import MagicMock, patch

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from motiprompt.screens import MainScreen


class TestMainScreen(unittest.TestCase):
    def setUp(self):
        self.my_root = MainScreen()
        self.my_root.quote_text = MagicMock(spec=Label)
        self.my_root.quote_author = MagicMock(spec=Label)
        self.my_root.random_quote = MagicMock(spec=GridLayout)

    @patch("motiprompt.screens.random.choice")
    @patch("motiprompt.screens.open")
    def test_get_quote_updates_labels(self, mock_open, mock_random_choice):
        # Mock the file content
        mock_file = MagicMock()
        mock_file.read.return_value = json.dumps([{"text": "Test Quote", "author": "Test Author"}])
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock random.choice to return a specific quote
        mock_random_choice.return_value = {
            "text": "Test Quote",
            "author": "Test Author",
        }

        # Call the method
        self.my_root.get_quote()

        # Ensure UI updates
        self.my_root.quote_text.texture_update()
        self.my_root.quote_author.texture_update()

        # Assert that the quote_text and quote_author labels are updated
        self.assertEqual(self.my_root.quote_text.text, '"Test Quote"')
        self.assertEqual(self.my_root.quote_author.text, "~ Test Author ~")

    def test_add_quote(self):
        # Mock the ScreenManager
        self.my_root.manager = MagicMock(spec=Screen)

        # Call the method
        self.my_root.add_quote()

        # Assert that the screen is switched to "add_quote"
        self.assertEqual(self.my_root.manager.current, "add_quote")

    def test_show_quotes(self):
        # Mock the ScreenManager
        self.my_root.manager = MagicMock(spec=Screen)

        # Call the method
        self.my_root.show_quotes()

        # Assert that the screen is switched to "show_quotes"
        self.assertEqual(self.my_root.manager.current, "show_quotes")
