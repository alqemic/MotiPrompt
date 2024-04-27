import json
import os
import random
import time
from sys import platform

import plyer
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
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

# from plyer import notification


class MyRoot(Screen):
    current_set = StringProperty("default")

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_widgets)
        Clock.schedule_once(self.create_dropdown)
        self.get_list_of_sets()

    def get_list_of_sets(self):
        self.quote_sets = [f.split(".")[0] for f in os.listdir("motiprompt/quotes") if f.endswith(".json")]

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

    def get_quote(self):
        with open(f"motiprompt/quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)
        rquote = random.choice(quotes)
        quote_text = rquote.get("text", "Unknown Text")
        quote_author = rquote.get("author", "Unknown Author")

        self.quote_text.text = f'"{quote_text}"'
        self.quote_author.text = f"~ {quote_author} ~"

    def notify_quote(self):
        if platform == "linux":
            plyer.utils.platform = "linux"  # only for testing purposes !!!
        plyer.notification.notify(
            title="Moti",
            message=f"{self.quote_text.text}\n~ {self.quote_author.text} ~",
            app_name="",
            app_icon="",
            timeout=10,
            ticker="",
            toast=False,
        )
        time.sleep(10)

    def add_quote(self):
        self.manager.current = "add_quote"

    def show_quotes(self):
        self.manager.current = "show_quotes"

    def settings(self):
        self.manager.current = "settings"


class AddQuote(Screen):
    current_set = StringProperty("default")

    def __init__(self, **kwargs):
        super(AddQuote, self).__init__(**kwargs)
        self.quote_sets = [f.split(".")[0] for f in os.listdir("motiprompt/quotes") if f.endswith(".json")]
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
        if os.path.exists(f"motiprompt/quotes/{new_set}.json"):
            self.show_error_dialog("Set already exists! Choose different name.")
            return
        self.current_set = new_set
        with open(f"motiprompt/quotes/{self.current_set}.json", "a") as file:
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

        with open(f"motiprompt/quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)

        quotes.append(new_quote)

        with open(f"motiprompt/quotes/{self.current_set}.json", "w") as file:
            json.dump(quotes, file, indent=2)

    def go_to_main(self):
        self.manager.current = "main"


class ShowQuotes(Screen):
    def __init__(self, **kwargs):
        super(ShowQuotes, self).__init__(**kwargs)
        self.bind(size=self._update_text_size)

        self.get_list_of_sets()
        self.current_set = "default"

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
        self.quote_sets = [f.split(".")[0] for f in os.listdir("motiprompt/quotes") if f.endswith(".json")]

    def refresh_quotes(self):
        self.layout.clear_widgets()
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
        self.build_dropdown_menu()

        self.layout.add_widget(self.dropdown_button)

        with open(f"motiprompt/quotes/{self.current_set}.json", "r") as file:
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
        grid.add_widget(Widget(size_hint_x=0.3))
        b = MDButton(on_press=self.go_to_main)
        b.add_widget(MDButtonIcon(icon="arrow-left"))
        b.add_widget(MDButtonText(text="Go Back"))
        grid.add_widget(b)
        grid.add_widget(Widget(size_hint_x=0.3))

        self.layout.add_widget(grid)

    def go_to_main(self, instance):
        self.manager.current = "main"

    def build_dropdown_menu(self):
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


class SettingsScreen(Screen):
    def save_settings(self):
        # notification_title = self.ids.notification_title.text
        # notification_message = self.ids.notification_message.text
        pass

    def go_to_main(self):
        self.manager.current = "main"
