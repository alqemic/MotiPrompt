import unittest
import json
from unittest.mock import patch, MagicMock

from motiprompt.screens import MyRoot


class TestMyRoot(unittest.TestCase):
    def setUp(self):
        self.my_root = MyRoot()

    @patch("motiprompt.screens.random.choice")
    @patch("motiprompt.screens.open")
    def test_get_quote(self, mock_open, mock_random_choice):
        # Mock the file content
        mock_file = MagicMock()
        mock_file.read.return_value = json.dumps(
            [{"text": "Test Quote", "author": "Test Author"}]
        )
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

    def test_generate_number(self):
        # Mock the min_val and max_val text fields
        self.my_root.min_val = MagicMock()
        self.my_root.min_val.text = "1"
        self.my_root.max_val = MagicMock()
        self.my_root.max_val.text = "10"

        # Mock random.randint
        with patch("motiprompt.screens.random.randint") as mock_randint:
            mock_randint.return_value = 5

            # Call the method
            self.my_root.generate_number()

        # Assert that the random_label is updated
        self.assertEqual(self.my_root.random_label.text, "5")
