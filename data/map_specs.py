import libtcodpy as libtcod

# max_monsters_per_room, max_items_per_room : table contenant table nb items/monstre, level donjon
# [[3,1], [5, 3]] = On part de la fin : Pour niveau 3+, 5 monstres. Pour niveau 1+, 3 monstres.

def get_map_config():
    config = {
        'standard_map': {
            'width': 80,
            'height': 43,
            'room_max_size': 10,
            'room_min_size': 5,
            'max_rooms': 30,
            'max_monsters_per_room': [[1, 1], [2, 3], [3, 6], [4, 10]],
            #'monster_table': 'standard_table',
            'max_items_per_room': [[1, 1], [2, 4], [3, 8]],
            'colors': {
                'dark_wall': libtcod.Color(0, 0, 100),
                'dark_ground': libtcod.Color(50, 50, 150),
                'light_wall': libtcod.Color(130, 110, 50),
                'light_ground': libtcod.Color(200, 180, 50)
            }
        },
        'forest_map': {
            'width': 80,
            'height': 43,
            'room_max_size': 7,
            'room_min_size': 5,
            'max_rooms': 30,
            'max_monsters_per_room': [[1, 1], [3, 3], [4, 6], [5, 10]],
            #'monster_table': 'standard_table',
            'max_items_per_room': [[1, 1], [2, 3], [3, 7]],
            'colors': {
                'dark_wall': libtcod.Color(20, 50, 50),
                'dark_ground': libtcod.Color(20, 100, 50),
                'light_wall': libtcod.Color(40, 125, 90),
                'light_ground': libtcod.Color(60, 175, 120)
            }
        },
        'old_forest': {
            'width': 80,
            'height': 43,
            'room_max_size': 9,
            'room_min_size': 5,
            'max_rooms': 30,
            'max_monsters_per_room': [[1, 1], [3, 3], [4, 6], [5, 10]],
            #'monster_table': 'standard_table',
            'max_items_per_room': [[1, 1], [2, 3], [3, 7]],
            'colors': {
                'dark_wall': libtcod.Color(20, 40, 60),
                'dark_ground': libtcod.Color(20, 90, 70),
                'light_wall': libtcod.Color(40, 105, 100),
                'light_ground': libtcod.Color(60, 155, 140)
            }
        },
        'thorns': {
            'width': 80,
            'height': 43,
            'room_max_size': 7,
            'room_min_size': 3,
            'max_rooms': 30,
            'max_monsters_per_room': [[1, 1], [3, 3], [4, 6], [5, 10]],
            #'monster_table': 'standard_table',
            'max_items_per_room': [[1, 1], [2, 3], [3, 7]],
            'colors': {
                'dark_wall': libtcod.Color(30, 30, 20),
                'dark_ground': libtcod.Color(30, 45, 25),
                'light_wall': libtcod.Color(60, 40, 40),
                'light_ground': libtcod.Color(60, 90, 50)
            }
        },
    }
    return config