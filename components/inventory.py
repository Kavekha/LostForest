from config.constants import ConstColors


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None

    def add_item(self, item):
        event_handler = self.owner.game.events
        if len(self.items) >= self.capacity:
            event_handler.add_event({'message': 'You cannot carry any more, your inventory is full',
                                     'color': ConstColors.INVENTORY_FULL})
        else:
            event_handler.add_event({'item_added': item})
            self.owner.game.dungeon.current_map.entities.remove(item)
            self.items.append(item)

    def no_item_found(self):
        event_handler = self.owner.game.events
        event_handler.add_event({'message': 'There is nothing here to pick up.',
                                 'color': ConstColors.NOTHING_TO_PICK_UP})

    def menu_options(self):
        header = 'Press the key next to an item to use it, or Esc to cancel.\n'
        if len(self.items) == 0:
            options = ['inventory is empty']
        else:
            options = [item.name for item in self.items]
        return header, options

    def use(self, item_entity, **kwargs):
        # print('inventory:use: item_ent, kwargs', item_entity, **kwargs)
        event_handler = self.owner.game.events

        item_component = item_entity.item

        if item_component.use_function is None:
            event_handler.add_event({'message': 'The {0} cannot be used'.format(item_entity.name),
                                     'color': ConstColors.CANNOT_BE_USED})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_result = item_component.use_function(self.owner, item_component.power, **kwargs)
            consume_item = item_use_result.get('consume_item')
            if consume_item:
                self.remove_item(item_entity)

            event_handler.add_event(item_use_result)

    def remove_item(self, item):
        self.items.remove(item)
