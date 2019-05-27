from config.constants import ConstColors, ConstTexts


'''
INVENTORY s'occupe de la gestion d'inventaire, la recuperation d'objets et leur utilisation.
Permets de centraliser les mecaniques generales d'usage d'items.

1. Player ouvre inventaire : menu.
2. Choisi l'item dans son inventaire.
3. inventory 'use' item:
    a. recupere la fonction associé à l'item.
    b. la lance.
    c. La fonction fait ses trucs 
    d. La fonction renvoie les Messages à afficher.
    e. La fonction renvoie aussi si "consume_item"
4. inventory recupere les messages & le consume_item
5. inventory envoie a Events les messages à afficher.
6. inventory consomme l'objet si necessaire.
'''

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None

    def add_item(self, item):
        event_handler = self.owner.game.events
        if len(self.items) >= self.capacity:
            event_handler.add_event({'message': ConstTexts.INVENTORY_FULL,
                                     'color': ConstColors.INVENTORY_FULL})
        else:
            event_handler.add_event({'message': 'You pick up the {0}!'.format(item.name),
                                     'color': ConstColors.ITEM_PICKED})
            self.owner.game.dungeon.current_map.entities.remove(item)
            self.items.append(item)

    def menu_options(self):
        header = ConstTexts.INVENTORY_HEADER
        if len(self.items) == 0:
            options = [ConstTexts.INVENTORY_EMPTY]
        else:
            options = [item.name for item in self.items]
        return header, options

    def use(self, item_entity, **kwargs):
        # Comment je communique les infos.
        event_handler = self.owner.game.events
        # J'utilise la partie "item" de l'entité.
        item_component = item_entity.item

        # L item que j utilise n a pas de fonctionnalité.
        if item_component.use_function is None:
            event_handler.add_event({'message': 'The {0} cannot be used'.format(item_entity.name),
                                     'color': ConstColors.CANNOT_BE_USED})

        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            # On recupere les messages de l'item pour les rendre à l utilisateur.
            # On obtient aussi si l item doit être consommé. Pas dans l effet du coup.
            item_use_result = item_component.use_function(self.owner, item_component.power, **kwargs)
            consume_item = item_use_result.get('consume_item')

            if consume_item:
                self.remove_item(item_entity)

            event_handler.add_event(item_use_result)

    def remove_item(self, item):
        self.items.remove(item)
