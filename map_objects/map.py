from map_objects.tile import Tile
from map_objects.rectangle import Rect
from config.config import get_map_config
from utils.fov_functions import initialize_fov
from spawners import Spawner
from components.stairs import Stairs
from entities import Entity
import libtcodpy as libtcod
from render_engine import RenderOrder

from random import randint


class GameMap:
    '''
    gère la creation de la map et son contenu, ainsi que sa mise à jour.
    '''
    def __init__(self, dungeon, map_type='standard_map'):
        # on recupere la configuration de la map, selon le type de map choisi par le jeu.
        self.map_type = map_type
        self.dungeon = dungeon

        map_config = get_map_config()
        self.colors = map_config[map_type]['colors']
        self.width = map_config[map_type]['width']
        self.height = map_config[map_type]['height']
        self.room_max_size = map_config[map_type]['room_max_size']
        self.room_min_size = map_config[map_type]['room_min_size']
        self.max_rooms = map_config[map_type]['max_rooms']
        self.max_monsters_room = map_config[map_type]['max_monsters_per_room']
        self.max_items_room = map_config[map_type]['max_items_per_room']

        # On créé une map pleine, non utilisable sans sa generation.
        self.tiles = self._initialize_tiles()   # tiles = la vraie map
        self.fov_map = None

        self.rooms = []
        self.entities = []

        # On genere un spawner, pour gerer le placement des mobs & items.
        self.spawner = Spawner(self)

    def add_player(self, player):
        self.entities.append(player)

    def add_entity(self, entity):
        self.entities.append(entity)

    def _initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    # On genere la map. # TODO : Pouvoir choisir la methode, selon que ce soit caverne, donj, etc.
    def generate_map(self, player):
        # La map en elle meme.
        self._make_map_tutorial_method(player)
        # Ce qui est visible ou non du joueur.
        self.fov_map = initialize_fov(self)
        # On spawn les entités qui la peuplent.
        self.spawner.spawn_entities()
        self.spawner.spawn_items()

    # La creation de la map basé sur le tutoriel Libtcod / Python.
    def _make_map_tutorial_method(self, player):
        rooms = []
        num_rooms = 0

        center_last_room_x = None
        center_last_room_y = None

        for r in range(self.max_rooms):
            # random width and height
            w = randint(self.room_min_size, self.room_max_size)
            h = randint(self.room_min_size, self.room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
                # we want to know the last created room for the stairs.
                center_last_room_x = new_x
                center_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon.current_floor + 1)
        down_stairs = Entity(self.dungeon, center_last_room_x, center_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        self.entities.append(down_stairs)

        self.rooms.extend(rooms)

    # creation d une salle. # TODO: Aujourd'hui, forcement un Rectangle. Personnalisable à faire?
    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    # tunnel horizontal, partant d'un point x1 vers un point x2, en restant sur l'horizon y
    # legere variété pour ne pas avoir un couloir de 1 tuile.   # TODO : rendre configurable, avec %
    def create_h_tunnel(self, x1, x2, y):
        rand = 0
        for x in range(min(x1, x2), max(x1, x2) + 1):
            rand += randint(-1, 1)
            if rand > 3:
                rand = 3
            elif rand < -3:
                rand = -3
            for i in range(min(0, rand), max(0, rand) + 1):
                self.tiles[x][y + i].blocked = False
                self.tiles[x][y + i].block_sight = False

    # tunnel vertical, partant de y1 vers y2, en restant sur vertical x.
    # legere variété pour ne pas avoir un couloir de 1 tuile.   # TODO : rendre configurable, avec %
    def create_v_tunnel(self, y1, y2, x):
        rand = 0
        for y in range(min(y1, y2), max(y1, y2) + 1):
            rand += randint(-1, 1)
            if rand > 3:
                rand = 3
            elif rand < -3:
                rand = -3
            for i in range(min(0, rand), max(0, rand) + 1):
                self.tiles[x + i][y].blocked = False
                self.tiles[x + i][y].block_sight = False
