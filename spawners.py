from random import randint
from entities import Entity
from data.monster_table import get_monster_table
from data.item_table import get_item_table
from data.monsters import get_monster_stats
from data.items import get_item_attributes
from components.fighter import Fighter
from components.item import Item
from render_engine import RenderOrder
from utils.random_functions import random_choice_from_dict


class Spawner:
    def __init__(self, map, max_monsters_room_table, max_items_room_table):
        self.map_owner = map
        self.max_monsters_room = self.from_dungeon_level(max_monsters_room_table, map.dungeon.current_floor)
        self.max_items_room = self.from_dungeon_level(max_items_room_table, map.dungeon.current_floor)
        self.monsters_table = get_monster_table(self.map_owner.map_type)
        self.items_table = get_item_table(self.map_owner.map_type)

    # table : [[nb_max, level],[nb_max, level + x]]
    # On donne le max, selon le niveau.
    # On retourne le bon nombre que l'on souhaite.
    def from_dungeon_level(self, table, dungeon_level):
        for (value, level) in reversed(table):
            if dungeon_level >= level:
                return value
        return 0

    def is_entity_there(self,x, y):
        # check if there is entity at this position
        if not any([entity for entity in self.map_owner.entities if entity.x == x and entity.y == y]):
            return False
        else:
            return True

    def spawn_entities(self):
        for room in self.map_owner.rooms:
            nb_monsters = randint(0, self.max_monsters_room)

            for mob in range(nb_monsters):
                x = randint(room.x1 + 1, room.x2 - 1)
                y = randint(room.y1 + 1, room.y2 - 1)

                # ici on check si il existe deja des entités à cet endroit.
                if not any([entity for entity in self.map_owner.entities if entity.x == x and entity.y == y]):
                    monster = self.spawn_monster(x, y)
                    self.map_owner.add_entity(monster)

    def spawn_monster(self, x, y):
        monster_list = self.monsters_table
        if monster_list:
            monster_name = random_choice_from_dict(monster_list)
            monster_stats = get_monster_stats(monster_name)
            if monster_stats:
                monster = self.create_monster(monster_name, x, y, monster_stats)
                return monster
            else:
                return None
        else:
            return None

    def spawn_items(self):
        for room in self.map_owner.rooms:
            nb_items = randint(0, self.max_items_room)
            for item in range(nb_items):
                x = randint(room.x1 + 1, room.x2 - 1)
                y = randint(room.y1 + 1, room.y2 - 1)

                if not self.is_entity_there(x, y):
                    item = self.spawn_item(x, y)
                    self.map_owner.add_entity(item)

    def spawn_item(self, x, y):
        item_list = self.items_table
        if item_list:
            item_name = random_choice_from_dict(item_list)
            item_attributes = get_item_attributes(item_name)
            if item_attributes:
                item_component = Item(item_attributes['use_function'], item_attributes['power'])
                game = self.map_owner.dungeon.game
                item = Entity(game,
                              x, y, item_attributes['char'], item_attributes['color'], item_name,
                              item=item_component,
                              render_order=RenderOrder.ITEM)
                return item
            else:
                return None

    def create_monster(self, monster_name, x, y, dict_stats):
        monster_appearance = dict_stats['char']
        monster_color = dict_stats['color']
        monster_hp = dict_stats['hp']

        ai_component = dict_stats['brain']
        fighter_component = Fighter(hp=monster_hp)
        # TODO: Pas ouf de remonter comme ca aussi haut pour recuperer le game.
        # TODO: Pertinence du Game dans Entity
        game = self.map_owner.dungeon.game
        monster = Entity(game,
                         x, y,
                         monster_appearance, monster_color, monster_name, blocks=True,
                         fighter=fighter_component,
                         ai=ai_component,
                         render_order=RenderOrder.ACTOR)
        return monster
