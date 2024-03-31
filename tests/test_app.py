import unittest

from motiprompt.main import MotiPrompt


class TestMotiPrompt(unittest.TestCase):
    def setUp(self):
        self.app = MotiPrompt()

    def test_appExists(self):
        assert self.app is not None
