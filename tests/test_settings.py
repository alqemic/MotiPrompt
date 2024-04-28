import unittest
from unittest.mock import MagicMock

from kivy.uix.screenmanager import Screen

from motiprompt.screens import SettingsScreen


class TestSettingsScreen(unittest.TestCase):
    def setUp(self):
        self.setscr = SettingsScreen()

    def test_go_to_main(self):
        # Mock the ScreenManager
        self.setscr.manager = MagicMock(spec=Screen)

        # Call the method
        self.setscr.go_to_main()

        # Assert that the screen is switched to "go_to_main"
        self.assertEqual(self.setscr.manager.current, "main")
