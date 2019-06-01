from config.constants import ConstColors, ConstTexts
from menus.inventory_menu import InventoryMenu


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

    def add_item(self, item, event_handler=None):
        if len(self.items) >= self.capacity:
            if event_handler:
                event_handler.add_event({'message': ConstTexts.INVENTORY_FULL, 'color': ConstColors.INVENTORY_FULL})
            return False
        else:
            if event_handler:
                event_handler.add_event({'message': 'You pick up the {0}!'.format(item.name),
                                         'color': ConstColors.ITEM_PICKED})
            self.owner.game.dungeon.current_map.entities.remove(item)
            self.items.append(item)
            return True

    def show_inventory(self):
        print('show inventory requested')
        game = self.owner.game
        game.current_menu = self.create_inventory_menu()

    def create_inventory_menu(self):
        inventory_menu = InventoryMenu(self)
        return inventory_menu

    def use(self, item_entity, **kwargs):
        # Comment je communique les infos.
        event_handler = self.owner.game.events
        # J'utilise la partie "item" de l'entité.
        item_component = item_entity.item

        # L item que j utilise n a pas de fonctionnalité.
        if item_component.use_function is None:
            event_handler.add_event({'message': 'The {0} cannot be used'.format(item_entity.name),
                                     'color': ConstColors.CANNOT_BE_USED})
            return False    # Can t be use

        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            # On recupere les messages de l'item pour les rendre à l utilisateur.
            # On obtient aussi si l item doit être consommé. Pas dans l effet du coup.
            item_use_result = item_component.use_function(self.owner, item_component.power, **kwargs)
            consume_item = item_use_result.get('consume_item')

            if consume_item:
                self.remove_item(item_entity)

            event_handler.add_event(item_use_result)
            return True     # Has been used

    def pick_up(self):
        event_handler = self.owner.game.events
        entities = self.owner.game.dungeon.current_map.entities
        for entity in entities:
            if entity.item and entity.x == self.owner.x and entity.y == self.owner.y:
                action_resolution = self.add_item(entity, event_handler)
                if action_resolution:
                    return True  # On indique que l'action est un succès.
                else:
                    break
        else:
            event_handler.add_event({'message': ConstTexts.NOTHING_TO_PICK_UP, 'color': ConstColors.NOTHING_TO_PICK_UP})
        return False    # On indique que l action n a pas reussi.

    def remove_item(self, item):
        self.items.remove(item)
