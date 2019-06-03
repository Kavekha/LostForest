from random import randint
from data.create_entities import create_entity_item, create_fighting_entity
from data.monster_table import get_monster_table
from data.item_table import get_item_table
from data.items import get_item_attributes
from utils.random_functions import random_choice_from_dict


class Spawner:
    def __init__(self, map, max_monsters_room_table, max_items_room_table):
        self.map_owner = map
        self.max_monsters_room = self.from_dungeon_level(max_monsters_room_table, map.dungeon.current_floor)
        self.max_items_room = self.from_dungeon_level(max_items_room_table, map.dungeon.current_floor)
        self.monsters_table = get_monster_table(self.map_owner.map_type)
        self.items_table = get_item_table(self.map_owner.map_type)

    # ADD & GET
    def _get_rooms(self):
        return self.map_owner.get_rooms()

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
        rooms = self._get_rooms()
        for room in rooms:
            nb_monsters = randint(0, self.max_monsters_room)

            for mob in range(nb_monsters):
                x = randint(room.x1 + 1, room.x2 - 1)
                y = randint(room.y1 + 1, room.y2 - 1)

                # ici on check si il existe deja des entités à cet endroit.
                if not any([entity for entity in self.map_owner.entities if entity.x == x and entity.y == y]):
                    monster = self.spawn_monster(x, y)
                    self.map_owner.add_entity(monster)

    def spawn_monster(self, x, y):
        game = self.map_owner.dungeon.game
        monster_list = self.monsters_table
        if monster_list:
            monster_name = random_choice_from_dict(monster_list)
            if monster_name:
                monster = create_fighting_entity(game, monster_name, x, y)
                return monster
        return None

    def spawn_items(self):
        rooms = self._get_rooms()
        for room in rooms:
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
                game = self.map_owner.dungeon.game
                item = create_entity_item(game, item_name, x, y, item_attributes)
                return item
        return None


