from utils.death_functions import kill_player, kill_monster
from config.constants import ConstColors
from game_messages import MessageLog


''' 
1. Fonction : Envoyer des messages.
2. Fonction : Gère aussi les events de type Mort, monster killed, item added, mais pas plein d'autres choses.
'''

# TODO: Clarifier si c'est un EventHandler ou un MessageHandler.
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
            color = event.get('color')

            if not color:
                color = ConstColors.NEUTRAL_INFO_COLOR

            if message:
                self.message_log.add_message(message, color)

            # TODO: Contournement pour gerer le dead_entity, kill_monster.
            # Surtout dû au fait qu'on file le game state PLAYER_DEAD via ce truc, hors ce n est pas son role.
            if information:
                self.message_log.add_message(information['text'], information['color'])

            if dead_entity:
                if dead_entity == self.game.player:
                    message, self.game.game_state = kill_player(dead_entity)
                    self.add_event({'information': {'text': message, 'color': ConstColors.YOU_ARE_DEAD}})
                else:
                    message = kill_monster(dead_entity)
                    self.add_event({'information': {'text': message, 'color': ConstColors.HOSTILE_KILLED}})

            if item_added:
                self.add_event({'information': {'text': 'You pick up the {0}!'.format(item_added.name),
                                'color': ConstColors.ITEM_PICKED}})

        self.reset_event_list()

    def reset_event_list(self):
        self.events = []
