import tcod as libtcod

import math

from data.map_specs import get_map_config
from utils.fov_functions import initialize_fov
from spawners import Spawner
from components.landmark import Landmark
from entities import Entity
from render_engine import RenderOrder
from map_generators.make_map import make_map
from map_generators.map_gen_consts import *


'''
{    
    'map_width': 80,
    'map_height': 60,
    'room_min_size': 3,
    'room_max_size': 5,
    'max_rooms': 30,
    'max_placement_iterations': 20,
    'max_iterations': 600,
    'corridor_chances': 0,
    'room_if_no_corridor': 0,
    'any_room_may_be_previous': 0,
    "min_mobs": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
    "max_mob_room": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
    "colors": {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150),
        "light_wall": libtcod.Color(130, 110, 50),
        "light_ground": libtcod.Color(200, 180, 50),
    }            
}
'''


class GameMap:
    """
    gère la creation de la map et son contenu, ainsi que sa mise à jour.
    """

    def __init__(self, dungeon, map_type="standard_map"):
        # on recupere la configuration de la map, selon le type de map choisi par le jeu.
        self.map_type = map_type
        self.dungeon = dungeon
        self.spawner = None

        self.tiles = None
        self.fov_map = None
        self.map_width = None
        self.map_height = None
        self.colors = None

        self._entities = []
        self._player = None
        self._items = []
        self._fighters = []
        self._rooms = []
        self._corridors = []

    def generate_map(self):
        # get config
        map_config = get_map_config(self.map_type)

        self.map_width = map_config.get('map_width', MAP_WIDTH)
        self.map_height = map_config.get('map_height', MAP_HEIGHT)

        self.colors = map_config.get('colors')

        map_elements = make_map(map_config)
        self.tiles = map_elements.get('tiles', False)
        self._rooms = map_elements.get('rooms', False)
        self._corridors = map_elements.get('corridors')

        self._player.x, self._player.y = self._rooms[0].center
        self.fov_map = initialize_fov(self)

        # create spawner and spawn word
        self.spawner = Spawner(self, map_config.get('min_mobs', [[2, 1]]), map_config.get('max_mob_room', [[3, 1]]),
                               map_config.get('min_items', [[0, 1]]), map_config.get('max_item_room', [[0, 1]]))
        self.place_landmark()
        self.spawner.spawn_entities()

    # ADD & GET.
    def get_map_sizes(self):
        return self.map_width, self.map_height

    def add_player(self, player):
        self._entities.append(player)
        self._player = player

    def add_entity(self, entity):
        self._entities.append(entity)

    def add_item(self, entity_item):
        self._items.append(entity_item)
        self.add_entity(entity_item)

    def add_fighters(self, entity_fighter):
        self._fighters.append(entity_fighter)
        self.add_entity(entity_fighter)

    def add_room(self, room):
        self._rooms.append(room)

    def add_corridor(self, corridor):
        self._corridors.append(corridor)

    def get_entities(self):
        return self._entities

    def get_items(self):
        return self._items

    def get_fighters(self):
        return self._fighters

    def get_rooms(self):
        return self._rooms

    def remove_entity(self, entity):
        if entity:
            self._entities.remove(entity)

    def remove_item(self, item):
        print('remove item from map - obsolete')

    def remove_fighter(self, fighter):
        print('remove fighter from map - obsolete')

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def is_indestructible(self, x, y):
        if self.tiles[x][y].destructible:
            return False
        return True

    def place_landmark(self):
        player_room = self.get_rooms()[0]
        farest_room = None
        farest_distance = 0
        for room in self.get_rooms():
            if room != player_room:
                distance = self.distance_room_to_room(player_room, room)
                if distance >= farest_distance:
                    print("farest distance : {} - room {}".format(distance, room))
                    farest_distance = distance
                    farest_room = room
            else:
                continue

        center_room_x, center_room_y = farest_room.center

        landmark_component = Landmark(self.dungeon.current_floor + 1)
        landmark = Entity(
            self.dungeon.game,
            center_room_x,
            center_room_y,
            ">",
            libtcod.yellow,
            "Landmark",
            render_order=RenderOrder.LANDMARK,
            landmark=landmark_component,
        )
        self.add_entity(landmark)

    # exist also in Entities
    def distance_room_to_room(self, room, other):
        dx1, dy1 = room.center
        dx2, dy2 = other.center

        dx = dx1 - dx2
        dy = dy1 - dy2

        return math.sqrt(dx ** 2 + dy ** 2)
