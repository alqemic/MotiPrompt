import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRoundFlatIconButton

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

        self.go_to_main()

    def go_to_main(self):
        self.manager.current = 'main'


class ShowQuotes(Screen):

    def __init__(self, **kwargs):
        super(ShowQuotes, self).__init__(**kwargs)
        self.bind(size=self._update_text_size)

        self.scroll_view = ScrollView()
        self.scroll_view.do_scroll_y = True
        self.scroll_view.do_scroll_x = True

        self.layout = BoxLayout(orientation='vertical')
        self.refresh_quotes()
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)

    def _update_text_size(self, instance, value):
        for child in self.layout.children:
            if isinstance(child, Label):
                child.text_size = (self.width, None)

    def on_enter(self, *args):
        self.refresh_quotes()

    def refresh_quotes(self):
        self.layout.clear_widgets()

        with open('motiprompt/quotes/default.json', 'r') as file:
            quotes = json.load(file)
        for quote in quotes:
            label = Label(text=f"{quote.get('text', 'Unknown Text')}\n ~ {quote.get('author', 'Unknown Author')} ~")
            label.text_size = (self.width, None)
            label.halign = 'center'
            label.valign = 'middle'
            label.height = label.texture_size[1] + 10
            self.layout.add_widget(label)

        grid= GridLayout(rows=1, cols=3)
        grid.add_widget(Widget(size_hint_x=0.3))
        grid.add_widget(MDRoundFlatIconButton(text='Go Back', on_press=self.go_to_main, icon='arrow-left'))
        grid.add_widget(Widget(size_hint_x=0.3))

        self.layout.add_widget(grid)

    def go_to_main(self, instance):
        self.manager.current = 'main'
