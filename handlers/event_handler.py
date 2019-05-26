from config.constants import ConstColors
from game_messages import MessageLog


''' 
Envoyer des messages.
Faire changer l'etat du jeu.
'''


class EventHandler:
    def __init__(self, game):
        self.events = []
        self.game = game
        self.message_log = MessageLog()

    def add_event(self, event):
        self.events.append(event)

    def resolve_events(self):
        for event in self.events:
            message = event.get('message')
            color = event.get('color')
            change_state = event.get('change_state')

            if not color:
                color = ConstColors.NEUTRAL_INFO_COLOR

            if message:
                self.message_log.add_message(message, color)

            if change_state:
                self.game.game_state = change_state

        self.reset_event_list()

    def reset_event_list(self):
        self.events = []
