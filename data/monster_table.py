def get_monster_table(map_type):
    tables = {
        'standard_map': {
            'ougloth': 10,
            'living root': 3
        },
        'forest_map': {
            'ougloth_weak': 30,
            'ougloth': 15,
            'living_root': 10,
            'charencon': 1,
            'gob_dog': 10,
            'murderous_root': 10
        },
        'old_forest': {
            'ougloth_weak': 22,
            'ougloth': 30,
            'ougloth_brute': 5,
            'living_root': 7,
            'charencon': 2,
            'gob_dog': 20,
            'murderous_root': 20
        },
        'thorns': {
            'ougloth_weak': 16,
            'ougloth': 22,
            'ougloth_brute': 10,
            'living_root': 5,
            'charencon': 4,
            'gob_dog': 15,
            'murderous_root': 15
        }
    }
    try:
        return tables[map_type]
    except:
        return None