from config.constants import ConstColors
from game_messages import MessageLog
from menus.victory_menu import VictoryMenu
from menus.level_menu import LevelUpMenu


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
            victory = event.get('victory')      # True
            level_up = event.get('level_up')    # Entity
            quit_target_mode = event.get('quit_target_mode')    # True
            function_to_play = event.get('function_to_play')    # function

            if not color:
                color = ConstColors.NEUTRAL_INFO_COLOR

            if message:
                self.message_log.add_message(message, color)

            if victory:
                self.game.current_menu = VictoryMenu()

            if level_up:
                self.game.current_menu = LevelUpMenu(level_up)

            if quit_target_mode:
                self.game.quit_target_mode()

            if function_to_play:
                function_to_play()

        self.reset_event_list()

    def reset_event_list(self):
        self.events = []
