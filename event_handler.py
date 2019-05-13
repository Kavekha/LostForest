from death_functions import kill_player, kill_monster


class EventHandler:
    def __init__(self, game):
        self.events = []
        self.game = game

    def add_event(self, event):
        self.events.append(event)

    def resolve_events(self):
        for event in self.events:
            message = event.get('message')
            dead_entity = event.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == self.game.player:
                    message, self.game.game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                print(message)

        self.reset_event_list()

    def reset_event_list(self):
        self.events = []
