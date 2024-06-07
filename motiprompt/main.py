import configparser
import json
import os

import kivy
from kivy.logger import Logger
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.uix.settings import SettingsWithTabbedPanel
from kivymd.app import MDApp
from screens import AddQuote, DeleteQuote, MainScreen, ShowQuotes

kivy.require("2.3.0")


class MotiScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MotiScreenManager, self).__init__(**kwargs)

        self.transition = FadeTransition()

        root = MainScreen(name="main")
        add_quote = AddQuote(name="add_quote")
        show_quotes = ShowQuotes(name="show_quotes")
        del_quote = DeleteQuote(name="delete_quote")

        self.add_widget(root)
        self.add_widget(add_quote)
        self.add_widget(show_quotes)
        self.add_widget(del_quote)


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

        self.sm = MotiScreenManager()
        return self.sm

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults("MotiPrompt", {"min_val": 7, "max_val": 20, "increment": 1, "selected_set": self.get_list_of_sets()[0]})

    def get_list_of_sets(self):
        """
        Get the list of available quote sets.
        """
        return sorted([f.split(".")[0] for f in os.listdir("quotes") if f.endswith(".json")])

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # Load the settings from the JSON file
        with open("settings.json", "r") as f:
            settings_data = json.load(f)

        # Update the options for the "selected_set" key
        for item in settings_data:
            if item["key"] == "selected_set":
                item["options"] = self.get_list_of_sets()

        # Write the updated settings back to the JSON file
        with open("settings.json", "w") as f:
            json.dump(settings_data, f, indent=4)

        settings.add_json_panel("MotiPrompt", self.config, filename="settings.json")

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
        config = configparser.ConfigParser()
        config.read("motiprompt.ini")
        self.sm.get_screen("main").increment = config.getint("MotiPrompt", "increment")
        self.sm.get_screen("main").start = config.getint("MotiPrompt", "min_val")
        self.sm.get_screen("main").end = config.getint("MotiPrompt", "max_val")
        self.sm.get_screen("main").selected_set = config.get("MotiPrompt", "selected_set")
        super(MotiPrompt, self).close_settings(settings)


if __name__ == "__main__":
    MotiPrompt().run()
