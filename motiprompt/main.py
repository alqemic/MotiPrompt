import kivy
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivymd.app import MDApp

from screens import AddQuote, MyRoot, SettingsScreen, ShowQuotes

kivy.require("2.3.0")


class MotiScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MotiScreenManager, self).__init__(**kwargs)

        self.transition = FadeTransition()

        root = MyRoot(name="main")
        add_quote = AddQuote(name="add_quote")
        show_quotes = ShowQuotes(name="show_quotes")
        settings = SettingsScreen(name="settings")

        self.add_widget(root)
        self.add_widget(add_quote)
        self.add_widget(show_quotes)
        self.add_widget(settings)


class MotiPrompt(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"

        sm = MotiScreenManager()
        return sm


if __name__ == "__main__":
    MotiPrompt().run()
