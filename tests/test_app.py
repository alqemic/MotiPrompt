import unittest

from kivy.uix.screenmanager import Screen

from motiprompt.main import MotiPrompt


class TestMotiPrompt(unittest.TestCase):
    def setUp(self):
        self.app = MotiPrompt()

    def test_appExists(self):
        assert self.app is not None

    def test_guiExists(self):
        gui = self.app.build()
        assert gui is not None

    def test_widgetsExists(self):
        gui = self.app.build()
        widgets = gui.children
        self.assertIsNotNone(widgets)
        self.assertEqual(len(widgets), 1)

    def test_screenExists(self):
        gui = self.app.build()
        widgets = gui.children
        screen = widgets[0]
        self.assertIsNotNone(screen)
        self.assertIsInstance(screen, Screen)
