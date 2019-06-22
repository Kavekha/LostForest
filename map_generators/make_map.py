from map_generators.jotaf_method import MapGeneratorJotaf
from map_generators.map_gen_consts import *

from map_objects.tile import Tile


def make_map(map_config):
    # tiles models
    terrain = {}

    map_width = map_config.get('map_width', MAP_WIDTH)
    map_height = map_config.get('map_height', MAP_HEIGHT)

    # create tiles
    create_tile_models(terrain)
    grid = initialize_grid(map_width, map_height)
    grid = initialize_tiles(grid, terrain, map_width, map_height)
    make_indestructible_barriers(grid, terrain, map_width, map_height)

    map_blueprint = get_map_blueprint(map_config)
    rooms, corridors = create_map(grid, terrain, map_blueprint)

    d_created_elements = {'tiles': grid, 'rooms': rooms, 'corridors': corridors, 'terrain': terrain}

    return d_created_elements


def create_map(grid, terrain, map_blueprint):
    rooms = []
    corridors = []

    rooms_to_create = map_blueprint.get('rooms')
    corridors_to_create = map_blueprint.get('corridors')

    for room in rooms_to_create:
        rooms.append(room)
        create_room(grid, terrain, room)

    for corridor in corridors_to_create:
        corridors.append(corridor)
        create_room(grid,terrain,  corridor)

    return rooms, corridors


def create_room(grid, terrain, room):
    # go through the tiles in the rectangle and make them passable
    for y in range(room.y1, room.y2):
        for x in range(room.x1, room.x2):
            if is_destructible(grid, x, y):
                grid[x][y] = terrain['ground']


def is_destructible(grid, x, y):
    if grid[x][y].destructible:
        return True
    return False


def get_map_blueprint(map_config):
    map_gen = map_config.get('map_algorithm', MapGeneratorJotaf)
    map_gen = map_gen(**map_config)
    map_gen.run()
    results = map_gen.get_results()
    return results


def make_indestructible_barriers(grid, terrain, map_width, map_height):
    for y in range(0, map_height):
        grid[0][y] = terrain['indestructible_wall']
        grid[map_width - 1][y] = terrain['indestructible_wall']

    for x in range(0, map_width):
        grid[x][0] = terrain['indestructible_wall']
        grid[x][map_height - 1] = terrain['indestructible_wall']


def initialize_grid(map_width, map_height):
        grid = [[None for y in range(map_height)] for x in range(map_width)]
        return grid


def initialize_tiles(grid, terrain, map_width, map_height):
    [[add_cell(grid, terrain['wall'], x, y) for y in range(map_height)] for x in range(map_width)]
    return grid


def create_tile_models(terrain):
    # all tiles, for now. Will be specified in map spec afterwards.
    # wall
    add_tile_type(terrain, 'wall', blocked=True, destructible=True)
    # ground
    add_tile_type(terrain, 'ground', False)
    # indestructible
    add_tile_type(terrain, 'indestructible_wall', True, destructible=False)


def add_tile_type(terrain, name, blocked, block_sight=None, destructible=False):
    # on créé la tuile dans terrain
    tile = Tile(name, blocked, block_sight, destructible, explored=False)
    terrain[name] = tile
    # on créé sa variante "explored"
    new_name = name + '_explored'
    tile_explored = Tile(new_name, blocked, block_sight, destructible, explored=True)
    terrain[new_name] = tile_explored


def add_cell(grid, tile, x, y):
    grid[x][y] = tile
