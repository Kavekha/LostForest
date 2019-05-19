import libtcodpy as libtcod


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None

    def add_item(self, item):
        event_handler = self.owner.game.events
        if len(self.items) >= self.capacity:
            event_handler.add_event({'information': {'text': 'You cannot carry any more, your inventory is full',
                                                     'color': libtcod.yellow}})
        else:
            event_handler.add_event({'item_added': item})
            self.owner.game.map.entities.remove(item)
            self.items.append(item)

    def no_item_found(self):
        event_handler = self.owner.game.events
        event_handler.add_event({'information': {'text': 'There is nothing here to pick up.',
                                                 'color': libtcod.yellow}})
