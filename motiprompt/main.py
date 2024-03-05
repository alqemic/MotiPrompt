import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import random

kivy.require('2.3.0')


class MyRoot(BoxLayout):

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)

    def generate_number(self):
        self.random_label.text = str(random.randint(0, 1000))


class MotiPrompt(App):

    def build(self):
        return MyRoot()


if __name__ == '__main__':
    MotiPrompt().run()
