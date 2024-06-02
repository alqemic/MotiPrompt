import configparser
import json
import os
import random
import time
from datetime import datetime
from sys import platform

import plyer
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField


class BaseScreen(Screen):
    quote_files = [f.split(".")[0] for f in os.listdir("quotes") if f.endswith(".json")]
    current_set = StringProperty(sorted(quote_files)[0]) if quote_files else StringProperty("")

    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.get_list_of_sets()

    def get_list_of_sets(self):
        self.quote_sets = sorted([f.split(".")[0] for f in os.listdir("quotes") if f.endswith(".json")])

    def go_to_main(self, *args):
        self.manager.current = "main"


class MainScreen(BaseScreen):
    increment = NumericProperty()
    start = NumericProperty()
    end = NumericProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_widgets)
        Clock.schedule_once(self.create_dropdown)

    def on_enter(self):
        self.get_list_of_sets()
        self.create_dropdown()

    def create_dropdown(self, *args):
        menu_items = [
            {
                "text": f"{item}",
                "on_release": lambda item=item: self.set_set(item),
            }
            for item in self.quote_sets
        ]
        self.dropdown_menu = MDDropdownMenu(items=menu_items, caller=self.ids.button)

    def set_set(self, set):
        self.current_set = set
        self.dropdown_menu.dismiss()

    def initialize_widgets(self, *args):
        self.quote_text = self.ids.quote_text
        self.quote_author = self.ids.quote_author
        self.random_quote = self.ids.random_quote
        if os.path.exists("motiprompt.ini"):
            config = configparser.ConfigParser()
            config.read("motiprompt.ini")
            self.increment = int(config.get("MotiPrompt", "increment"))
            self.start = int(config.get("MotiPrompt", "min_val"))
            self.end = int(config.get("MotiPrompt", "max_val"))

    def get_quote(self):
        with open(f"quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)
        rquote = random.choice(quotes)
        quote_text = rquote.get("text", "Unknown Text")
        quote_author = rquote.get("author", "Unknown Author")

        self.quote_text.text = f'"{quote_text}"'
        self.quote_author.text = f"~ {quote_author} ~"

    def notify_quote(self):
        if plyer.utils.platform == "android":
            from plyer.platforms.android.notification import AndroidNotification
            from plyer.platforms.android.vibrator import AndroidVibrator

            while True:
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

    def add_quote(self):
        self.manager.current = "add_quote"

    def show_quotes(self):
        self.manager.current = "show_quotes"

    def delete_quote(self):
        self.manager.current = "delete_quote"

    def exit_app(self):
        MDApp.get_running_app().stop()


class AddQuote(BaseScreen):
    def __init__(self, **kwargs):
        super(AddQuote, self).__init__(**kwargs)
        Clock.schedule_once(self.create_dropdown)

    def create_dropdown(self, *args):
        menu_items = []
        for item in self.quote_sets:
            menu_items.append(
                {
                    "text": f"{item}",
                    "on_release": lambda item=item: self.set_set(item),
                }
            )
        menu_items.append(
            {
                "text": "Create new set",
                "on_release": self.show_dialog,
            }
        )
        self.dropdown_menu = MDDropdownMenu(items=menu_items, caller=self.ids.button)

    def set_set(self, set):
        self.current_set = set
        self.dropdown_menu.dismiss()

    def show_dialog(self):
        self.new_set_name = MDTextField()
        create_button = MDButton(MDButtonText(text="Create"), on_release=self.create_set, style="text")
        cancel_button = MDButton(MDButtonText(text="Cancel"), on_release=self.dismiss_dialog, style="text")
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Create new set"),
            MDDialogSupportingText(text="Enter the name of the new set, e.g. 'my_set'"),
            MDDialogContentContainer(self.new_set_name),
            MDDialogButtonContainer(Widget(), create_button, cancel_button, spacing="8dp"),
        )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dropdown_menu.dismiss()
        self.dialog.dismiss()

    def create_set(self, instance):
        new_set = str(self.new_set_name.text)
        if not new_set:
            self.show_error_dialog("Set name cannot be empty!")
            return
        if any(c.isspace() for c in new_set):
            self.show_error_dialog("Set name cannot contain spaces!")
            return
        if os.path.exists(f"quotes/{new_set}.json"):
            self.show_error_dialog("Set already exists! Choose different name.")
            return
        self.current_set = new_set
        with open(f"quotes/{self.current_set}.json", "a") as file:
            json.dump([], file, indent=2)
        self.dismiss_dialog()

    def show_error_dialog(self, message):
        ok_button = MDButton(MDButtonText(text="OK"), on_release=self.dismiss_error_dialog, style="text")
        button_box = BoxLayout(orientation="vertical")
        button_box.add_widget(ok_button)
        self.error_dialog = MDDialog(
            MDDialogHeadlineText(text="Error"),
            MDDialogSupportingText(text=message),
            MDDialogButtonContainer(Widget(), button_box, Widget()),
        )
        self.error_dialog.open()

    def dismiss_error_dialog(self, *args):
        self.error_dialog.dismiss()

    def save_quote(self):
        new_quote = {
            "text": self.new_quote_text.text,
            "author": self.new_quote_author.text,
        }

        with open(f"quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)

        quotes.append(new_quote)

        with open(f"quotes/{self.current_set}.json", "w") as file:
            json.dump(quotes, file, indent=2)


class ShowQuotes(BaseScreen):
    def __init__(self, **kwargs):
        super(ShowQuotes, self).__init__(**kwargs)
        self.bind(size=self._update_text_size)
        self.layout = BoxLayout(orientation="vertical")

        self.refresh_quotes()
        self.add_widget(self.layout)

    def _update_text_size(self, instance, value):
        for child in self.layout.children:
            if isinstance(child, Label):
                child.text_size = (self.width, None)

    def on_enter(self, *args):
        self.get_list_of_sets()
        self.refresh_quotes()

    def get_list_of_sets(self):
        self.quote_sets = sorted([f.split(".")[0] for f in os.listdir("quotes") if f.endswith(".json")])

    def refresh_quotes(self):
        self.layout.clear_widgets()

        self.header = GridLayout(cols=2)
        self.header.add_widget(Image(source="assets/icon.png", size_hint_y=1, size_hint_x=0.2, height=self.layout.height))
        self.header.add_widget(Label(text="Show Quotes", font_size=72, color=(0.92, 0.45, 0, 1), size_hint_y=1))
        self.layout.add_widget(self.header)

        items = [{"text": f} for f in self.quote_sets]
        self.dropdown_button = MDButton(
            pos_hint={"center_x": 0.5, "center_y": 0.9},
        )
        self.dropdown_menu = MDDropdownMenu(
            caller=self.dropdown_button,
            items=items,
        )
        self.dropdown_button.bind(on_release=lambda instance: self.dropdown_menu.open())
        self.dropdown_button.add_widget(MDButtonIcon(icon="menu"))
        self.dropdown_button.add_widget(MDButtonText(text=self.current_set))
        self.create_dropdown()

        self.layout.add_widget(self.dropdown_button)

        with open(f"quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)
        for quote in quotes:
            label = Label(
                text=f"{quote.get('text', 'Unknown Text')}\n ~ {quote.get('author', 'Unknown Author')} ~",
                text_size=(self.width, None),
                halign="center",
                valign="middle",
            )
            self.layout.add_widget(label)

        grid = GridLayout(rows=1, cols=3)
        grid.add_widget(Widget(size_hint=(self.width * 0.3, self.height)))
        b = MDButton(on_press=self.go_to_main)
        b.size_hint = self.width * 0.3, self.height
        b.add_widget(MDButtonIcon(icon="arrow-left"))
        b.add_widget(MDButtonText(text="Go Back"))
        grid.add_widget(b)
        grid.add_widget(Widget(size_hint=(self.width * 0.3, self.height)))

        self.layout.add_widget(grid)

    def create_dropdown(self):
        self.dropdown_menu.items = [
            {
                "text": quote_set,
                "on_release": lambda x=quote_set: self.select_quote_set(x),
            }
            for quote_set in self.quote_sets
        ]

    def select_quote_set(self, quote_set):
        self.current_set = quote_set
        self.dropdown_button.text = f"Select Set: {quote_set}"
        self.dropdown_menu.dismiss()
        self.refresh_quotes()


class DeleteQuote(BaseScreen):
    def __init__(self, **kwargs):
        super(DeleteQuote, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_widgets)

    def initialize_widgets(self, *args):
        self.box = self.ids.box
        self.dquotes = self.ids.dquotes

    def on_enter(self, *args):
        self.get_list_of_sets()
        self.refresh_quotes()

    def get_list_of_sets(self):
        self.quote_sets = sorted([f.split(".")[0] for f in os.listdir("quotes") if f.endswith(".json")])

    def create_dropdown(self, *args):
        self.dropdown_menu.items = [
            {
                "text": quote_set,
                "on_release": lambda x=quote_set: self.select_quote_set(x),
            }
            for quote_set in self.quote_sets
        ]

    def select_quote_set(self, quote_set):
        self.current_set = quote_set
        self.dropdown_button.text = f"Select Set: {quote_set}"
        self.dropdown_menu.dismiss()
        self.refresh_quotes()

    def refresh_quotes(self):
        self.dquotes.clear_widgets()

        items = [{"text": f} for f in self.quote_sets]
        self.dropdown_button = MDButton(
            style="tonal",
            pos_hint={"center_x": 0.5, "center_y": 0.9},
        )
        self.dropdown_menu = MDDropdownMenu(
            caller=self.dropdown_button,
            items=items,
        )
        self.dropdown_button.bind(on_release=lambda instance: self.dropdown_menu.open())
        self.dropdown_button.add_widget(MDButtonIcon(icon="menu"))
        self.dropdown_button.add_widget(MDButtonText(text=self.current_set))
        self.create_dropdown()

        self.dquotes.add_widget(self.dropdown_button)

        with open(f"quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)
        for quote in quotes:
            b = MDButton(
                size_hint=(self.box.width, None),
                on_press=self.show_confirmation_dialog,
            )
            bt = MDButtonText(text=f"{quote.get('text', 'Unknown Text')} ~ {quote.get('author', 'Unknown Author')} ~")
            b.add_widget(bt)
            self.dquotes.add_widget(b)

    def show_confirmation_dialog(self, instance):
        yes_button = MDButton(MDButtonText(text="Yes"), on_release=self.delete_quote, style="text")
        no_button = MDButton(MDButtonText(text="No"), on_release=self.dismiss_confirmation_dialog, style="text")
        button_box = BoxLayout(orientation="horizontal")
        button_box.add_widget(yes_button)
        button_box.add_widget(no_button)
        for child in instance.children:
            if isinstance(child, MDButtonText):
                self.quote_text = child.text
                break
        self.confirmation_dialog = MDDialog(
            MDDialogHeadlineText(text="Do you want to delete this quote?"),
            MDDialogSupportingText(text=self.quote_text),
            MDDialogButtonContainer(Widget(), button_box, Widget()),
        )
        self.confirmation_dialog.open()

    def dismiss_confirmation_dialog(self, *args):
        self.confirmation_dialog.dismiss()

    def delete_quote(self, instance):
        with open(f"quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)
        if len(quotes) <= 1:
            self.delete_set_confirmation()
        else:
            for i, quote in enumerate(quotes):
                if f"{quote.get('text', 'Unknown Text')} ~ {quote.get('author', 'Unknown Author')} ~" == self.quote_text:
                    del quotes[i]
                    break
            with open(f"quotes/{self.current_set}.json", "w") as file:
                json.dump(quotes, file, indent=2)
        self.dismiss_confirmation_dialog()
        self.refresh_quotes()

    def delete_set_confirmation(self):
        yes_button = MDButton(MDButtonText(text="Yes"), on_release=self.delete_set, style="text")
        no_button = MDButton(MDButtonText(text="No"), on_release=self.dismiss_set_confirmation_dialog, style="text")
        button_box = BoxLayout(orientation="horizontal")
        button_box.add_widget(yes_button)
        button_box.add_widget(no_button)
        self.set_confirmation_dialog = MDDialog(
            MDDialogHeadlineText(text="Do you want to delete this set?"),
            MDDialogSupportingText(text=f"This is the last quote in '{self.current_set}'. Set will be deleted."),
            MDDialogButtonContainer(Widget(), button_box, Widget()),
        )
        self.set_confirmation_dialog.open()

    def dismiss_set_confirmation_dialog(self, *args):
        self.set_confirmation_dialog.dismiss()

    def delete_set(self, *args):
        os.remove(f"quotes/{self.current_set}.json")
        self.get_list_of_sets()
        for s in self.manager.screens:
            s.current_set = sorted([f.split(".")[0] for f in os.listdir("quotes") if f.endswith(".json")])[0]
        self.refresh_quotes()
        self.set_confirmation_dialog.dismiss()
