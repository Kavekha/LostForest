import libtcodpy as libtcod


def get_app_config():
    configuration = {
        'version': '0.0.9',
        'screen_width': 80,
        'screen_height': 50,
        'bar_width': 20,
        'panel_height': 7
    }
    return configuration


def get_game_config():
    config = {
        'fov_algorithm': 0
    }

    return config


def get_map_config():
    config = {
        'standard_map': {
            'width': 80,
            'height': 43,
            'room_max_size': 10,
            'room_min_size': 5,
            'max_rooms': 30,
            'max_monsters_per_room': 2,
            'monster_table': 'standard_table',
            'max_items_per_room': 1,
            'colors': {
                'dark_wall': libtcod.Color(0, 0, 100),
                'dark_ground': libtcod.Color(50, 50, 150),
                'light_wall': libtcod.Color(130, 110, 50),
                'light_ground': libtcod.Color(200, 180, 50)
            }
        }
    }
    return config
