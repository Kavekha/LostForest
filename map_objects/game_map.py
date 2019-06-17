import math
from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect

from data.map_specs import get_map_config

from utils.fov_functions import initialize_fov
from spawners import Spawner
from components.landmark import Landmark
from entities import Entity
import tcod as libtcod
from render_engine import RenderOrder
from map_generators.jotaf_method import MapGeneratorJotaf


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
        self.map_width, self.map_height = map_config.get('map_width'), map_config.get('map_height')
        self.colors = map_config.get('colors')
        # this is the MapGen, map_config is the **params. Return Rooms & corridors to create.
        map_blueprint = self.get_map_blueprint(map_config)

        # initialize map
        self.tiles = self._initialize_tiles(self.map_width, self.map_height)
        # Tiles indestructibles autour.
        self._make_indestructible_barriers(self.map_width, self.map_height)
        self.fov_map = None

        # make map
        self._make_map(map_blueprint)
        self._player.x, self._player.y = self._rooms[0].center
        self.fov_map = initialize_fov(self)

        # create spawner and spawn word
        self.spawner = Spawner(self, map_config.get('min_mobs', [[2, 1]]), map_config.get('max_mob_room', [[3, 1]]),
                               map_config.get('min_items', [[0, 1]]), map_config.get('max_item_room', [[0, 1]]))
        self.place_landmark()
        self.spawner.spawn_entities()

    def _make_map(self, map_blueprint):
        rooms_to_create = map_blueprint.get('rooms')
        corridors_to_create = map_blueprint.get('corridors')

        for room in rooms_to_create:
            self.add_room(room)
            self.create_room(room)
        for corridor in corridors_to_create:
            self.add_corridor(corridor)
            self.create_room(corridor)

    def get_map_blueprint(self, map_config):
        map_gen = map_config.get('map_algorithm', MapGeneratorJotaf)
        map_gen = map_gen(**map_config)
        map_gen.run()
        results = map_gen.get_results()
        return results

    # MAP CREATION
    def _initialize_tiles(self, map_width, map_height):
        tiles = [[Tile(True) for y in range(map_height)] for x in range(map_width)]

        for x in range(map_width):
            for y in range(map_height):
                pass

        return tiles

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

    def _make_indestructible_barriers(self, map_width, map_height):
        for y in range(0, map_height):
            self.tiles[0][y].destructible = False
            self.tiles[map_width - 1][y].destructible = False

        for x in range(0, map_width):
            self.tiles[x][0].destructible = False
            self.tiles[x][map_height - 1].destructible = False

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

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for y in range(room.y1, room.y2):
            for x in range(room.x1, room.x2):
                if self.tiles[x][y].destructible:
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False
