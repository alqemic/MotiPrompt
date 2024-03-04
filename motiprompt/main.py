import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MotiPrompt(App):

    def build(self):
        return BoxLayout()


if __name__ == '__main__':
    MotiPrompt().run()
