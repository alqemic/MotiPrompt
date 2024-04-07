import json
import os
import random

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


class MyRoot(Screen):
    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        self.quote_text = Label()
        self.quote_author = Label()
        self.random_quote = GridLayout()

    def get_quote(self):
        with open("motiprompt/quotes/default.json", "r") as file:
            quotes = json.load(file)
        rquote = random.choice(quotes)
        quote_text = rquote.get("text", "Unknown Text")
        quote_author = rquote.get("author", "Unknown Author")

        self.quote_text.text = f'"{quote_text}"'
        self.quote_author.text = f"~ {quote_author} ~"

    def add_quote(self):
        self.manager.current = "add_quote"

    def show_quotes(self):
        self.manager.current = "show_quotes"


class AddQuote(Screen):
    current_set = StringProperty("default")

    def __init__(self, **kwargs):
        super(AddQuote, self).__init__(**kwargs)
        self.quote_sets = [f.split(".")[0] for f in os.listdir("motiprompt/quotes") if f.endswith(".json")]
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
        self.dropdown1 = MDDropdownMenu(items=menu_items, width_mult=4, caller=self.ids.button)

    def set_set(self, set):
        self.current_set = set
        self.dropdown1.dismiss()

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
        self.dropdown1.dismiss()
        self.dialog.dismiss()

    def create_set(self, instance):
        self.current_set = str(self.new_set_name.text)
        with open(f"motiprompt/quotes/{self.current_set}.json", "a") as file:
            json.dump([], file, indent=2)
        self.dismiss_dialog()

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

        self.quote_sets = [f.split(".")[0] for f in os.listdir("motiprompt/quotes") if f.endswith(".json")]
        self.current_set = "default"

        self.layout = BoxLayout(orientation="vertical")

        self.refresh_quotes()
        self.add_widget(self.layout)

    def _update_text_size(self, instance, value):
        for child in self.layout.children:
            if isinstance(child, Label):
                child.text_size = (self.width, None)

    def on_enter(self, *args):
        self.refresh_quotes()

    def refresh_quotes(self):
        self.layout.clear_widgets()
        items = [{"text": f} for f in self.quote_sets]
        self.dropdown_button = MDButton(
            pos_hint={"center_x": 0.5, "center_y": 0.9},
        )
        self.dropdown_menu = MDDropdownMenu(
            caller=self.dropdown_button,
            items=items,
            width_mult=4,
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
        self.dropdown_menu.items.clear()
        for quote_set in self.quote_sets:
            self.dropdown_menu.items.append(
                {
                    "text": quote_set,
                    "on_release": lambda x=quote_set: self.select_quote_set(x),
                }
            )

    def select_quote_set(self, quote_set):
        self.current_set = quote_set
        self.dropdown_button.text = f"Select Set: {quote_set}"
        self.dropdown_menu.dismiss()
        self.refresh_quotes()
