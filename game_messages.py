import libtcodpy as libtcod
import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self):
        self.messages = []
        self.history = []

    def add_message(self, message, color=libtcod.white):
        print(message)
        self.messages.append(Message(message, color))
        if len(self.messages) > 5:
            self.add_history(self.messages[0])
            del self.messages[0]

    def add_history(self, old_message):
        self.history.append(old_message)
