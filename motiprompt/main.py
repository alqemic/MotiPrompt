import json
import kivy
from kivy.app import App
from kivy.config import ConfigParser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import random

kivy.require('2.3.0')


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


class MyRoot(Screen):

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)

    def get_quote(self):
        with open('motiprompt/quotes/default.json', 'r') as file:
            quotes = json.load(file)
        rquote = random.choice(quotes)
        quote_text = rquote.get('text', 'Unknown Text')
        quote_author = rquote.get('author', 'Unknown Author')

        self.quote_text.text = f'"{quote_text}"'
        self.quote_author.text = f'~ {quote_author} ~'

    def generate_number(self):
        self.random_label.text = str(random.randint(int(self.min_val.text), int(self.max_val.text)))

    def add_quote(self):
        self.manager.current = 'add_quote'


class AddQuote(Screen):

    def __init__(self, **kwargs):
        super(AddQuote, self).__init__(**kwargs)

    def save_quote(self):
        new_quote = {
            "text": self.new_quote_text.text,
            "author": self.new_quote_author.text
        }

        with open('motiprompt/quotes/default.json', 'r') as file:
            quotes = json.load(file)

        quotes.append(new_quote)

        with open('motiprompt/quotes/default.json', 'w') as file:
            json.dump(quotes, file, indent=2)

        self.manager.current = 'main'


class MotiPrompt(App):

    def build(self):
        self.settings_cls = SettingsWithTabbedPanel

        # We apply the saved configuration settings or the defaults
        root = MyRoot(name='main')
        root.ids.min_val.text = self.config.get('My Settings', 'min_val')
        root.ids.max_val.text = self.config.get('My Settings', 'max_val')

        # Create the screen manager and add the main and add_quote screens
        sm = ScreenManager()
        sm.add_widget(root)
        sm.add_widget(AddQuote(name='add_quote'))

        # Set the root widget to the screen manager
        # root.manager = sm
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
            if key == "min_val":
                self.root.ids.min_val.text = value
            elif key == "max_val":
                self.root.ids.max_val.text = value

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MotiPrompt, self).close_settings(settings)


if __name__ == '__main__':
    MotiPrompt().run()
