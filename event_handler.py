from utils.death_functions import kill_player, kill_monster
from game_messages import MessageLog
import libtcodpy as libtcod


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
            dead_entity = event.get('dead')
            information = event.get('information')
            item_added = event.get('item_added')

            if message:
                self.message_log.add_message(message)

            if information:
                print('information is ', information)
                self.message_log.add_message(information['text'], information['color'])

            if dead_entity:
                if dead_entity == self.game.player:
                    message, self.game.game_state = kill_player(dead_entity)
                    self.add_event({'information': {'text': message, 'color': libtcod.red}})
                else:
                    message = kill_monster(dead_entity)
                    self.add_event({'information': {'text': message, 'color': libtcod.orange}})

            if item_added:
                self.add_event({'information': {'text': 'You pick up the {0}!'.format(item_added.name),
                                'color': libtcod.light_blue}})

        self.reset_event_list()

    def reset_event_list(self):
        self.events = []
