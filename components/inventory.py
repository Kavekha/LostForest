from config import color_config
from systems.localization import Texts
from menus.inventory_menu import InventoryMenu, DropMenu
from components.equippable import get_equipment_in_slot


"""
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
"""


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None

    def add_item(self, item, event_handler=None):
        if len(self.items) >= self.capacity:
            if event_handler:
                event_handler.add_event(
                    {
                        "message": Texts.get_text('INVENTORY_FULL'),
                        "color": color_config.INVENTORY_FULL,
                    }
                )
            return False
        else:
            if event_handler:
                event_handler.add_event(
                    {
                        "message": Texts.get_text('PICK_UP_ITEM').format(item.name),
                        "color": color_config.ITEM_PICKED,
                    }
                )
            self.owner.game.dungeon.current_map.get_entities().remove(item)
            self.items.append(item)
            return True

    def action_take_round(self):
        self.owner.end_turn()

    def show_inventory(self, action):
        if action == "use":
            menu = self.create_inventory_menu()
        elif action == "drop":
            menu = self.create_drop_menu()
        else:
            raise NotImplementedError

        game = self.owner.game
        game.current_menu = menu

    def create_drop_menu(self):
        drop_menu = DropMenu(self)
        return drop_menu

    def create_inventory_menu(self):
        inventory_menu = InventoryMenu(self)
        return inventory_menu

    def drop(self, item_entity):
        event_handler = self.owner.game.events
        game_map = self.owner.game.dungeon.current_map

        if (
            item_entity.equippable
            and self.owner.equipment
            and item_entity
            == get_equipment_in_slot(item_entity.equippable.slot, self.owner.equipment)
        ):
            self.owner.equipment.toggle_equip(item_entity)
        else:
            item_entity.x, item_entity.y = self.owner.x, self.owner.y
            game_map.add_entity(item_entity)
            self.remove_item(item_entity)
            event_handler.add_event(
                {
                    "message": Texts.get_text('DROP_ITEM').format(item_entity.name),
                    "color": color_config.ITEM_DROPED,
                }
            )
        return True  # please update menu

    def use(self, item_entity):
        event_handler = self.owner.game.events
        item_component = item_entity.item
        if item_entity.equippable:
            equippable_component = item_entity.equippable
        else:
            equippable_component = None

        # Equipable item and can be equip by inventory owner
        if equippable_component and self.owner.equipment:
            self.owner.equipment.toggle_equip(item_entity)
            self.action_take_round()
            return True  # has been equipped

        # L item que j utilise n a pas de fonctionnalité.
        elif item_component.use_function is None:
            event_handler.add_event(
                {
                    "message": Texts.get_text('CANNOT_USE_ITEM').format(item_entity.name),
                    "color": color_config.CANNOT_BE_USED,
                }
            )
            return False  # Can t be use

        # L item a une fonctionnalité.
        elif item_component.use_function:
            # Target!
            target_type = item_component.target_type
            game = self.owner.game
            game.activate_target_mode(item_component, target_type)

        else:
            raise NotImplementedError

    def resolve_use_results(self, item_use_results, item_used_entity, event_handler):
        event_handler.add_event(item_use_results)

        consume_item = item_use_results.get("consume_item")

        if consume_item:
            self.remove_item(item_used_entity)
            self.action_take_round()
            return True  # item used, please refresh Menu
        return False

    def pick_up(self):
        event_handler = self.owner.game.events
        entities = self.owner.game.dungeon.current_map.get_entities()
        for entity in entities:
            if entity.item and entity.x == self.owner.x and entity.y == self.owner.y:
                action_resolution = self.add_item(entity, event_handler)
                if action_resolution:
                    return True  # On indique que l'action est un succès.
                else:
                    break
        else:
            event_handler.add_event(
                {
                    "message": Texts.get_text('NOTHING_TO_PICK_UP'),
                    "color": color_config.NOTHING_TO_PICK_UP,
                }
            )
        return False  # On indique que l action n a pas reussi.

    def remove_item(self, item):
        self.items.remove(item)
