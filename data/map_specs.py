import tcod as libtcod

from map_generators.jotaf_method import MapGeneratorJotaf
from map_generators.broguelike_method import MapGeneratorBrogueLike

# max_monsters_per_room, max_items_per_room : table contenant table nb items/monstre, level donjon
# [[3,1], [5, 3]] = On part de la fin : Pour niveau 3+, 5 monstres. Pour niveau 1+, 3 monstres.


def get_map_config(map_name):
    config = {
        "standard_map": {
            'map_algorithm': MapGeneratorJotaf,
            'map_width': 80,
            'map_height': 43,
            'room_min_size': 5,
            'room_max_size': 7,
            'max_rooms': 30,
            'max_placement_iterations': 20,
            'max_iterations': 600,
            'corridor_chances': 0,
            'room_if_no_corridor': 0,
            'any_room_may_be_previous': 0,
            "min_mobs": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "max_mob_room": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "min_items": [[10, 1]],
            "max_item_room": [[3, 1]],
            "colors": {
                "dark_wall": 'standard_dark_wall',
                "dark_ground": 'standard_dark_ground',
                "light_wall": 'standard_light_wall',
                "light_ground": 'standard_light_ground'
            },
        },
        "forest_map": {
            'map_algorithm': MapGeneratorBrogueLike,
            'map_width': 80,
            'map_height': 43,
            'room_min_size': 5,
            'room_max_size': 7,
            'max_rooms': 40,
            'max_placement_iterations': 20,
            'max_iterations': 600,
            'corridor_chances': 90,
            'room_if_no_corridor': 10,
            'any_room_may_be_previous': 20,
            "min_mobs": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "max_mob_room": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "min_items": [[10, 1]],
            "max_item_room": [[3, 1]],
            "colors": {
                "dark_wall": 'forest_dark_wall', # libtcod.Color(20, 50, 50),
                "dark_ground": 'forest_dark_ground', # libtcod.Color(20, 100, 50),
                "light_wall": 'forest_light_wall', # libtcod.Color(40, 125, 90),
                "light_ground": 'forest_light_ground'   # libtcod.Color(60, 175, 120),
            },
        },
        "old_forest": {
            'map_algorithm': MapGeneratorBrogueLike,
            'map_width': 80,
            'map_height': 43,
            'room_min_size': 5,
            'room_max_size': 7,
            'max_rooms': 40,
            'max_placement_iterations': 20,
            'max_iterations': 600,
            'corridor_chances': 90,
            'room_if_no_corridor': 10,
            'any_room_may_be_previous': 20,
            "min_mobs": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "max_mob_room": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "min_items": [[10, 1]],
            "max_item_room": [[3, 1]],
            "colors": {
                "dark_wall": 'old_forest_dark_wall',
                "dark_ground": 'old_forest_dark_ground',
                "light_wall": 'old_forest_light_wall',
                "light_ground": 'old_forest_light_ground'
            },
        },
        "thorns": {
            'map_algorithm': MapGeneratorBrogueLike,
            'map_width': 80,
            'map_height': 43,
            'room_min_size': 5,
            'room_max_size': 7,
            'max_rooms': 40,
            'max_placement_iterations': 20,
            'max_iterations': 600,
            'corridor_chances': 90,
            'room_if_no_corridor': 10,
            'any_room_may_be_previous': 20,
            "min_mobs": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "max_mob_room": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
            "min_items": [[10, 1]],
            "max_item_room": [[3, 1]],
            "colors": {
                "dark_wall": 'thorns_dark_wall',
                "dark_ground": 'thorns_dark_ground',
                "light_wall": 'thorns_light_wall',
                "light_ground": 'thorns_light_ground'
            },
        },
    }
    return config[map_name]
