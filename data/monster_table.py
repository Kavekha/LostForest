def get_monster_table(map_type):
    tables = {
        'standard_map': {
            'ougloth': 10,
            'living root': 3
        },
        'forest_map': {
            'ougloth_weak': 30,
            'ougloth': 5,
            'living_root': 10,
            'gob_dog': 10,
            'murderous_root': 10
        },
        'old_forest': {
            'ougloth_weak': 20,
            'ougloth': 10,
            'ougloth_brute': 3,
            'living_root': 4,
            'charencon': 1,
            'gob_dog': 20,
            'murderous_root': 20
        },
        'thorns': {
            'ougloth_weak': 14,
            'ougloth': 20,
            'ougloth_brute': 6,
            'living_root': 2,
            'charencon': 2,
            'gob_dog': 14,
            'murderous_root': 14
        }
    }
    try:
        return tables[map_type]
    except:
        return None