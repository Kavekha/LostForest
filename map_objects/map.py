from map_objects.tile import Tile
from map_objects.rectangle import Rect
from data.map_specs import get_map_config
from utils.fov_functions import initialize_fov
from spawners import Spawner
from components.stairs import Stairs
from entities import Entity
import libtcodpy as libtcod
from render_engine import RenderOrder

import math
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
        # for spawner
        max_monsters_room_table = map_config[map_type]['max_monsters_per_room']
        max_items_room_table = map_config[map_type]['max_items_per_room']

        # On créé une map pleine, non utilisable sans sa generation.
        self.tiles = self._initialize_tiles()   # tiles = la vraie map
        self._make_indestructible_barriers()    # Tiles indestructibles autour.
        self.fov_map = None

        self._rooms = []
        self.entities = []
        self._player = None
        self._items = []
        self._fighters = []

        # On genere un spawner, pour gerer le placement des mobs & items.
        self.spawner = Spawner(self, max_monsters_room_table, max_items_room_table)

    # ADD & GET.
    def add_player(self, player):
        self.entities.append(player)
        self._player = player

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_item(self, entity_item):
        self._items.append(entity_item)
        self.add_entity(entity_item)

    def add_fighters(self, entity_fighter):
        self._fighters.append(entity_fighter)
        self.add_entity(entity_fighter)

    def add_room(self, room):
        self._rooms.append(room)

    def get_entities(self):
        return self.entities

    def get_items(self):
        return self._items

    def get_fighters(self):
        return self._fighters

    def get_rooms(self):
        return self._rooms

    def remove_entity(self, entity):
        try:
            self.entities.remove(entity)
        except:
            raise IndexError

    def remove_item(self, item):
        if item.item:   # component Item
            try:
                self._items.remove(item)
                self.remove_entity(item)
            except:
                raise IndexError
        else:
            raise AssertionError

    def remove_fighter(self, fighter):
        if fighter.fighter:
            try:
                self._fighters.remove(fighter)
                self.remove_entity(fighter)
            except:
                raise IndexError
        else:
            raise AssertionError

    # MAP CREATION
    def _initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        for x in range(self.width):
            for y in range(self.height):
                pass

        return tiles

    def _make_indestructible_barriers(self):
        for y in range(0, self.height):
            self.tiles[0][y].destructible = False
            self.tiles[self.width - 1][y].destructible = False

        for x in range(0, self.width):
            self.tiles[x][0].destructible = False
            self.tiles[x][self.height - 1].destructible = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def is_indestructible(self, x, y):
        if self.tiles[x][y].destructible:
            return False
        return True

    # On genere la map. # TODO : Pouvoir choisir la methode, selon que ce soit caverne, donj, etc.
    def generate_map(self, player):
        # La map en elle meme.
        self._make_map_tutorial_method(player)
        self.place_stairs()
        # Ce qui est visible ou non du joueur.
        self.fov_map = initialize_fov(self)
        # On spawn les entités qui la peuplent.
        self.spawner.spawn_entities()
        self.spawner.spawn_items()

    # La creation de la map basé sur le tutoriel Libtcod / Python.
    def _make_map_tutorial_method(self, player):
        rooms = []
        num_rooms = 0

        '''
        center_last_room_x = None
        center_last_room_y = None
        '''

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
                '''
                # we want to know the last created room for the stairs.
                center_last_room_x = new_x
                center_last_room_y = new_y
                '''

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

        for room in rooms:
            self.add_room(room)

    def place_stairs(self):
        player_room = self.get_rooms()[0]
        farest_room = None
        farest_distance = 0
        for room in self.get_rooms():
            if room != player_room:
                distance = self.distance_room_to_room(player_room, room)
                if distance >= farest_distance:
                    print('farest distance : {} - room {}'.format(distance, room))
                    farest_distance = distance
                    farest_room = room
            else:
                continue

        center_room_x, center_room_y = farest_room.center()

        stairs_component = Stairs(self.dungeon.current_floor + 1)
        down_stairs = Entity(self.dungeon.game, center_room_x, center_room_y, '>', libtcod.yellow, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        self.entities.append(down_stairs)

    # exist also in Entities
    def distance_room_to_room(self, room, other):
        dx1, dy1 = room.center()
        dx2, dy2 = other.center()

        dx = dx1 - dx2
        dy = dy1 - dy2

        return math.sqrt(dx ** 2 + dy ** 2)

    # creation d une salle. # TODO: Aujourd'hui, forcement un Rectangle. Personnalisable à faire?
    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                if self.tiles[x][y].destructible:
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False
                else:
                    print('tile {},{} is indestructible : {}'.format(x, y, self.tiles[x][y].destructible))

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
                if self.tiles[x][y + i].destructible:
                    self.tiles[x][y + i].blocked = False
                    self.tiles[x][y + i].block_sight = False
                else:
                    print('self tile is indestructible')

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
                if self.tiles[x + i][y].destructible:
                    self.tiles[x + i][y].blocked = False
                    self.tiles[x + i][y].block_sight = False
                else:
                    print('self tile is indestructible')
