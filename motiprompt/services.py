import configparser
import json
import os
import random
import time
from datetime import datetime
from sys import platform

import plyer
from android.runnable import run_on_ui_thread
from jnius import autoclass
from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty

Service = autoclass("org.kivy.android.PythonService")
PythonService = autoclass("org.kivy.android.PythonService").mService


class QuoteService(Service):
    increment = NumericProperty()
    start = NumericProperty()
    end = NumericProperty()
    selected_set = StringProperty()

    def __init__(self, **kwargs):
        super(QuoteService, self).__init__(**kwargs)
        self.initialize_widgets()
        self.get_quote()

    def initialize_widgets(self, *args):
        if os.path.exists("motiprompt.ini"):
            config = configparser.ConfigParser()
            config.read("motiprompt.ini")
            self.increment = int(config.get("MotiPrompt", "increment"))
            self.start = int(config.get("MotiPrompt", "min_val"))
            self.end = int(config.get("MotiPrompt", "max_val"))
            self.selected_set = config.get("MotiPrompt", "selected_set")

    def get_quote(self):
        with open(f"quotes/{self.selected_set}.json", "r") as f:
            quotes = json.load(f)
        rquote = random.choice(quotes)
        quote_text = rquote.get("text", "Unknown Text")
        quote_author = rquote.get("author", "Unknown Author")

        self.quote_text = f'"{quote_text}"'
        self.quote_author = f"~ {quote_author} ~"

    @run_on_ui_thread
    def notify_quote(self):
        if plyer.utils.platform == "android":
            from plyer.platforms.android.notification import AndroidNotification
            from plyer.platforms.android.vibrator import AndroidVibrator

            while self.start <= datetime.now().hour < self.end:
                self.get_quote()
                current_time = datetime.now().strftime("%H:%M")
                AndroidNotification().notify(
                    title="MotiPrompt",
                    message=f"{self.quote_text} {self.quote_author} {current_time}",
                    app_name="",
                    app_icon="",
                    timeout=10,
                    ticker="",
                    toast=False,
                )
                AndroidVibrator().vibrate(0.1)
                time.sleep(self.increment * 3600)
        else:
            Logger.info(f"Moti: Notifications not supported for platform: '{platform}'")

    def start(self, *args):
        self.notify_quote()

    def stop(self, *args):
        pass

    def on_start(self):
        self.start()

    def on_stop(self):
        self.stop()


if __name__ == "__main__":
    service = QuoteService()
    service.notify_quote()
