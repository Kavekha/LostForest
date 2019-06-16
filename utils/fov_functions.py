import tcod as libtcod


def initialize_fov(game_map):
    width, height = game_map.get_map_sizes()
    fov_map = libtcod.map_new(width, height)

    for y in range(height):
        for x in range(width):
            libtcod.map_set_properties(
                fov_map,
                x,
                y,
                not game_map.tiles[x][y].block_sight,
                not game_map.tiles[x][y].blocked,
            )
    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)


def discover_new_tiles(game_map):
    width, height = game_map.get_map_sizes()
    for y in range(height):
        for x in range(width):
            visible = libtcod.map_is_in_fov(game_map.fov_map, x, y)
            if visible:
                game_map.tiles[x][y].explored = True
