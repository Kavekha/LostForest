from random import randint
from data.create_entities import create_entity_item, create_fighting_entity
from data.monster_table import get_monster_table
from data.item_table import get_item_table
from data.items import get_item_attributes
from utils.random_functions import random_choice_from_dict


class Spawner:
    def __init__(self, game_map, max_monsters_room_table, max_items_room_table, danger_level, value_level):
        self.map_owner = game_map
        self.max_monsters_room = self.from_dungeon_level(max_monsters_room_table, game_map.dungeon.current_floor)
        self.max_items_room = self.from_dungeon_level(max_items_room_table, game_map.dungeon.current_floor)
        self.monsters_table = get_monster_table(self.map_owner.map_type)
        self.items_table = get_item_table(self.map_owner.map_type)
        self.danger_level = self.from_dungeon_level(danger_level, game_map.dungeon.current_floor)
        self.value_level = self.from_dungeon_level(value_level, game_map.dungeon.current_floor)

    # ADD & GET
    def _get_rooms(self):
        return self.map_owner.get_rooms()

    def spawn_entities(self):
        rooms = self._get_rooms()
        start_room = rooms[0]
        nb_mobs_by_room = []
        nb_items_by_room = []

        # Il nous faut le nombre de mobs par room
        for room in rooms:
            if room == start_room:
                nb_mobs_by_room.append(0)
                nb_items_by_room.append(0)
            else:
                nb_monsters = randint(0, self.max_monsters_room)
                nb_items = randint(0, self.max_items_room)
                nb_mobs_by_room.append(nb_monsters)
                nb_items_by_room.append(nb_items)

        current_danger_level = 0
        current_item_value = 0

        for i in range(len(rooms)):
            if nb_mobs_by_room[i] > 0 and current_danger_level < self.danger_level:
                x = randint(rooms[i].x1 + 1, rooms[i].x2 - 1)
                y = randint(rooms[i].y1 + 1, rooms[i].y2 - 1)

                if not any([entity for entity in self.map_owner.entities if entity.x == x and entity.y == y]):
                    monster = self.spawn_monster(x, y)
                    self.map_owner.add_entity(monster)
                    current_danger_level += monster.fighter.xp_value
                    nb_mobs_by_room[i] -= 1

            if nb_items_by_room[i] > 0 and current_item_value < self.value_level:
                x = randint(rooms[i].x1 + 1, rooms[i].x2 - 1)
                y = randint(rooms[i].y1 + 1, rooms[i].y2 - 1)

                if not any([entity for entity in self.map_owner.entities if entity.x == x and entity.y == y]):
                    item = self.spawn_item(x, y)
                    self.map_owner.add_entity(item)
                    current_item_value += item.item.value
                    nb_items_by_room[i] -= 1

        print('END OF SPAWNING : danger lvl {}, monsters not spawner : {}'.format(current_danger_level,
                                                                                  sum(nb_mobs_by_room)))
        print('END OF SPAWNING : current value {}, items not spawner : {}'.format(current_item_value,
                                                                                  sum(nb_items_by_room)))

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

    # OBSOLETE v0.0.22
    def old_spawn_entities(self):
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


