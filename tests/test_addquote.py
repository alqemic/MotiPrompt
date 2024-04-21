import json
import unittest
from unittest.mock import MagicMock, patch

from kivy.uix.screenmanager import Screen

from motiprompt.screens import AddQuote


class TestAddQuote(unittest.TestCase):
    def setUp(self):
        self.addq = AddQuote()

    def test_go_to_main(self):
        # Mock the ScreenManager
        self.addq.manager = MagicMock(spec=Screen)

        # Call the method
        self.addq.go_to_main()

        # Assert that the screen is switched to "go_to_main"
        self.assertEqual(self.addq.manager.current, "main")

    def test_save_quote(self):
        # Mock the input values
        self.addq.new_quote_text = MagicMock()
        self.addq.new_quote_text.text = "This is a new quote"
        self.addq.new_quote_author = MagicMock()
        self.addq.new_quote_author.text = "John Doe"

        # Mock the file operations
        with patch("builtins.open") as mock_open:
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__exit__.return_value = None
            mock_open.return_value = mock_file

            # Mock the existing quotes
            existing_quotes = [{"text": "Existing quote", "author": "Jane Doe"}]
            mock_file.read.return_value = json.dumps(existing_quotes)

            # Call the method
            self.addq.save_quote()

            # Assert that the new quote is added
            expected_quotes = existing_quotes + [{"text": "This is a new quote", "author": "John Doe"}]
            expected_json = json.dumps(expected_quotes, indent=2)

            # Collect all the arguments passed to write
            write_calls = "".join(call[0][0] for call in mock_file.write.call_args_list)

            # Assert that write was called with the expected JSON string
            self.assertEqual(write_calls, expected_json)
