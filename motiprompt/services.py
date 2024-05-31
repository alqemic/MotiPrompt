import time
from datetime import datetime
from sys import platform

import plyer
from android.runnable import run_on_ui_thread
from jnius import autoclass
from kivy.logger import Logger

Service = autoclass("org.kivy.android.PythonService")
PythonService = autoclass("org.kivy.android.PythonService").mService


class QuoteService(Service):
    @run_on_ui_thread
    def notify_quote(self):
        if plyer.utils.platform == "android":
            from plyer.platforms.android.notification import AndroidNotification
            from plyer.platforms.android.vibrator import AndroidVibrator

            while self.running:
                self.get_quote()
                current_time = datetime.now().strftime("%H:%M")
                AndroidNotification().notify(
                    title="Moti",
                    message=f"{self.quote_text.text}\n{self.quote_author.text}\n{current_time}",
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
        self.running = True
        self.notify_quote()

    def stop(self, *args):
        self.running = False

    def on_start(self):
        self.start()

    def on_stop(self):
        self.stop()
