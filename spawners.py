from random import randint
from create_entities import create_entity_item, create_fighting_entity
from data.monster_table import get_monster_table
from data.item_table import get_item_table
from data.items import get_item_attributes
from utils.random_functions import random_choice_from_dict
from config import map_gen_config


class Spawner:
    def __init__(self, game_map, min_mobs, max_mob_room, min_items, max_item_room):
        self.map_owner = game_map
        self.monsters_table = get_monster_table(self.map_owner.map_type)
        self.items_table = get_item_table(self.map_owner.map_type)

        self.min_mobs = self.from_dungeon_level(min_mobs, game_map.dungeon.current_floor)
        self.max_mob_room = self.from_dungeon_level(max_mob_room, game_map.dungeon.current_floor)

        self.min_items = self.from_dungeon_level(min_items, game_map.dungeon.current_floor)
        self.max_item_room = self.from_dungeon_level(max_item_room, game_map.dungeon.current_floor)

    # ADD & GET
    def get_rooms(self):
        return self.map_owner.get_rooms()

    def spawn_entities(self):
        self.spawn_creatures()
        self.spawn_items()

    def spawn_items(self):
        min_items = self.min_items
        max_item_room = self.max_item_room

        rooms = self.get_rooms()
        start_room = rooms[0]

        item_by_room = [0 for i in range(len(rooms) - 1)]

        # on s assure que min mobs est atteignable.
        while (len(rooms) * max_item_room) < min_items:
            max_item_room += 1

        iteration = 0
        while sum(item_by_room) < min_items and iteration < 20:
            for i in range(len(rooms) - 1):
                if rooms[i] is not start_room and item_by_room[i] < max_item_room:
                    rand = randint(0, 1)
                    item_by_room[i] += rand
            iteration += 1

        for i in range(len(rooms) - 1):
            while item_by_room[i] > 0:
                x = randint(rooms[i].x1 + 1, rooms[i].x2 - 1)
                y = randint(rooms[i].y1 + 1, rooms[i].y2 - 1)

                if not any(
                        [
                            entity
                            for entity in self.map_owner.get_entities()
                            if entity.x == x and entity.y == y
                        ]
                ):
                    item = self.spawn_item(x, y)
                    if item:
                        self.map_owner.add_entity(item)
                    item_by_room[i] -= 1

    def spawn_creatures(self):
        min_mobs = self.min_mobs
        max_mob_room = self.max_mob_room

        rooms = self.get_rooms()
        start_room = rooms[0]

        monster_by_room = [0 for i in range(len(rooms) - 1)]

        # on s assure que min mobs est atteignable.
        while (len(rooms) * max_mob_room) < min_mobs:
            max_mob_room += 1

        iteration = 0
        while sum(monster_by_room) < min_mobs and iteration < 20:
            for i in range(len(rooms) - 1):
                if rooms[i] is not start_room and monster_by_room[i] < max_mob_room:
                    rand = randint(0, 1)
                    monster_by_room[i] += rand
            iteration += 1

        for i in range(len(rooms) - 1):
            while monster_by_room[i] > 0:
                x = randint(rooms[i].x1 + 1, rooms[i].x2 - 1)
                y = randint(rooms[i].y1 + 1, rooms[i].y2 - 1)

                if not any(
                    [
                        entity
                        for entity in self.map_owner.get_entities()
                        if entity.x == x and entity.y == y
                    ]
                ):
                    monster = self.spawn_monster(x, y)
                    if monster:
                        self.map_owner.add_entity(monster)
                    monster_by_room[i] -= 1

    # table : [[nb_max, level],[nb_max, level + x]]
    # On donne le max, selon le niveau.
    # On retourne le bon nombre que l'on souhaite.
    def from_dungeon_level(self, table, dungeon_level):
        for (value, level) in reversed(table):
            if dungeon_level >= level:
                return value
        return 0

    def is_entity_there(self, x, y):
        # check if there is entity at this position
        if not any(
            [
                entity
                for entity in self.map_owner.entities
                if entity.x == x and entity.y == y
            ]
        ):
            return False
        else:
            return True

    def spawn_monster(self, x, y):
        game = self.map_owner.dungeon.game
        map_type = self.map_owner.map_type
        monster_name = self.get_last_object_from_table(map_type, get_monster_table)
        if monster_name:
            monster = create_fighting_entity(game, monster_name, x, y)
            if monster:
                return monster
        return None

    def spawn_item(self, x, y):
        map_type = self.map_owner.map_type
        item_name = self.get_last_object_from_table(map_type, get_item_table)
        item_attributes = get_item_attributes(item_name)
        if item_attributes:
            game = self.map_owner.dungeon.game
            item = create_entity_item(game, item_name, x, y)
            return item
        return None

    def get_last_object_from_table(self, key, func_get_table):
        key_received = key
        count = 0
        while True and count < map_gen_config.MAX_TABLE_ITERATIONS:
            key_received, stop_searching = self.get_object_from_table(key_received, func_get_table)
            count +=1
            if stop_searching:
                break
        return key_received

    def get_object_from_table(self, key, func_get_table):
        # by default, this is the map type, used as key for dict item table
        # we want to know if there is another item table in it.
        try:
            # Est ce que la table item contient "key"? => Si oui
            current_table = func_get_table(key)
            # Pas d except, donc la table contenait une key vers une autre table de item_table:
            object_returned = random_choice_from_dict(current_table)
            return object_returned, False
        except:
            return key, True






