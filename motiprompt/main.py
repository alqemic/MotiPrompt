import kivy
from kivy.app import App
from kivy.config import ConfigParser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.lang import Builder

import random

kivy.require('2.3.0')

# This JSON defines entries we want to appear in our App configuration screen
json = '''
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

class MyRoot(BoxLayout):

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)

    def generate_number(self):
        self.random_label.text = str(random.randint(self.min_val, self.max_val))


class MotiPrompt(App):

    def build(self):
        self.settings_cls = MySettingsWithTabbedPanel

        # We apply the saved configuration settings or the defaults
        root = MyRoot()
        min_val = int(self.config.get('My Settings', 'min_val'))
        max_val = int(self.config.get('My Settings', 'max_val'))
        root.min_val = min_val
        root.max_val = max_val
        return root

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('My Settings', {'min_val': 0, 'max_val': 10})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Settings', self.config, 'settings.json')
        settings.add_json_panel('My Settings', self.config, data=json)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "My Settings":
            if key == "min_val":
                self.root.ids.min_val = int(value)
            elif key == "max_val":
                self.root.ids.max_val = int(value)

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MotiPrompt, self).close_settings(settings)

# Settings
        

class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):

    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))

if __name__ == '__main__':
    MotiPrompt().run()
