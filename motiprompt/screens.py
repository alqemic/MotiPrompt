import json
import os
import random

from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
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
    def __init__(self, **kwargs):
        super(AddQuote, self).__init__(**kwargs)
        self.current_set = "default"
        menu_items = []
        for item in [each.split(".")[0] for each in os.listdir("motiprompt/quotes")]:
            menu_items.append(
                {
                    "text": f"{item}",
                    "on_release": lambda *args: self.set_set(item),
                }
            )
        menu_items.append(
            {
                "text": "Create new set",
                "on_release": lambda *args: self.new_set(),
            }
        )
        self.dropdown1 = MDDropdownMenu(items=menu_items, width_mult=4, caller=self.ids.button)

    def set_set(self, set):
        # Last item from the list passed instead of the selected
        Logger.info(f"current set before: {set} {self.current_set}")
        self.current_set = set
        Logger.info(f"current set after: {set} {self.current_set}")

    def new_set(self):
        self.new_set_name = MDTextField(
            id="new_quote_set",
            text="New set name",
            helper_text="New set name, e.g. 'my_set'",
            multiline=False,
        )
        create_button = MDButton(on_press=self.create_set)
        create_button.add_widget(MDButtonText(text="Create"))

        self.new_set_grid = GridLayout(rows=1, cols=2)
        self.new_set_grid.add_widget(self.new_set_name)
        self.new_set_grid.add_widget(create_button)
        self.add_widget(self.new_set_grid)

    def create_set(self, instance):
        self.current_set = str(self.new_set_name.text)
        with open(f"motiprompt/quotes/{self.current_set}.json", "a") as file:
            json.dump([], file, indent=2)

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

        self.quote_sets = ["default", "set1", "set2"]
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
        Logger.info("ShowQuotes: Creating dropdown menu")
        self.dropdown_menu = MDDropdownMenu(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            width_mult=4,
        )
        Logger.info("ShowQuotes: Creating dropdown button")
        self.dropdown_button = MDButton(
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            on_release=self.dropdown_menu.open,
        )
        self.dropdown_button.add_widget(MDButtonIcon(icon="menu"))
        self.dropdown_button.add_widget(MDButtonText(text=self.current_set))
        self.build_dropdown_menu()

        self.layout.add_widget(self.dropdown_button)

        with open(f"motiprompt/quotes/{self.current_set}.json", "r") as file:
            quotes = json.load(file)
        for quote in quotes:
            label = Label(text=f"{quote.get('text', 'Unknown Text')}\n ~ {quote.get('author', 'Unknown Author')} ~")
            label.text_size = (self.width, None)
            label.halign = "center"
            label.valign = "middle"
            label.height = label.texture_size[1] + 10
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
        self.refresh_quotes()
        self.dropdown_menu.dismiss()
