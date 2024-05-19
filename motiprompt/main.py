import kivy
from kivy.logger import Logger
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.uix.settings import SettingsWithTabbedPanel
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


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_config_change: " "{0}, {1}, {2}, {3}".format(config, section, key, value))


class MotiPrompt(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"

        self.settings_cls = MySettingsWithTabbedPanel

        sm = MotiScreenManager()
        return sm

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults("My Settings", {"min_val": 0, "max_val": 10})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel("My Settings", self.config, data="[]")

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(config, section, key, value))

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MotiPrompt, self).close_settings(settings)


if __name__ == "__main__":
    MotiPrompt().run()
