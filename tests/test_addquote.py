import unittest
from unittest.mock import MagicMock

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
