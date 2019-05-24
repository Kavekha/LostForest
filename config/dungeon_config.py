def get_dungeon_config(dungeon_name='dungeon'):
    config = {
        'dungeon': {
            'max_floor': 10
        }
    }
    return config[dungeon_name]
