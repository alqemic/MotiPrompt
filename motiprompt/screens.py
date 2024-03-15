import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

import random


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

    def show_quotes(self):
        self.manager.current = 'show_quotes'


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


class ShowQuotes(Screen):

    def __init__(self, **kwargs):
        super(ShowQuotes, self).__init__(**kwargs)

        # Create a ScrollView to hold the quotes
        self.scroll_view = ScrollView()
        self.scroll_view.do_scroll_y = True
        self.scroll_view.do_scroll_x = True

        # Create a BoxLayout to hold the quotes
        self.layout = BoxLayout(orientation='vertical')


        # Add a label for each quote
        with open('motiprompt/quotes/default.json', 'r') as file:
            quotes = json.load(file)
        for quote in quotes:
            self.layout.add_widget(Label(text=f"{quote.get('text', 'Unknown Text')} - {quote.get('author', 'Unknown Author')}"))

        # Add a button to go back to the main screen
        self.layout.add_widget(Button(text='Back', on_press=self.go_to_main))

        # Add the BoxLayout to the ScrollView
        self.scroll_view.add_widget(self.layout)

        # Add the BoxLayout to the screen
        self.add_widget(self.scroll_view)

    def go_to_main(self, instance):
        self.manager.current = 'main'
