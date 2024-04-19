import unittest
from unittest.mock import MagicMock

from kivy.uix.screenmanager import Screen

from motiprompt.screens import ShowQuotes


class TestShowQuotes(unittest.TestCase):
    def setUp(self):
        self.showq = ShowQuotes()

    def test_go_to_main(self):
        # Mock the ScreenManager
        self.showq.manager = MagicMock(spec=Screen)

        # Call the method
        self.showq.go_to_main(MagicMock)

        # Assert that the screen is switched to "go_to_main"
        self.assertEqual(self.showq.manager.current, "main")
