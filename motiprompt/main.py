
import kivy
from kivy.core.window import Window
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from motiprompt.screens import AddQuote, MyRoot, ShowQuotes

kivy.require('2.3.0')

Window.clearcolor = (0.5, 0.5, 0.5, 1)
Window.size = (600, 700)

settings_json = '''
[
    {
        "type": "numeric",
        "title": "Minimum",
        "desc": "Choose the minimum value for random generator",
        "section": "My Settings",
        "key": "min_val"
    },
    {
        "type": "numeric",
        "title": "Maximum",
        "desc": "Choose the maximum value for random generator",
        "section": "My Settings",
        "key": "max_val"
    }
]
'''

class MotiPrompt(MDApp):

    def build(self):
        self.settings_cls = SettingsWithTabbedPanel
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        root = MyRoot(name='main')
        root.ids.min_val.text = self.config.get('My Settings', 'min_val')
        root.ids.max_val.text = self.config.get('My Settings', 'max_val')

        add_quote = AddQuote(name='add_quote')
        show_quotes = ShowQuotes(name='show_quotes')

        sm = ScreenManager()
        sm.add_widget(root)
        sm.add_widget(add_quote)
        sm.add_widget(show_quotes)

        return sm

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('My Settings', {'min_val': 0, 'max_val': 10})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel('My Settings', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "My Settings":
            match key:
                case "min_val":
                    self.root.ids.min_val.text = value
                case "max_val":
                    self.root.ids.max_val.text = value

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MotiPrompt, self).close_settings(settings)


if __name__ == '__main__':
    MotiPrompt().run()
