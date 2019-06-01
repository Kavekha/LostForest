def get_monster_table(map_type):
    tables = {
        'standard_map': {
            'ougloth': 10,
            'living root': 3
        },
        'forest_map': {
            'ougloth_weak': 10,
            'ougloth': 10,
            'living_root': 10,
            'charencon': 1,
            'gob_dog': 9,
            'murderous_root': 10
        },
        'old_forest': {
            'ougloth_weak': 7,
            'ougloth': 13,
            'ougloth_brute': 3,
            'living_root': 7,
            'charencon': 2,
            'gob_dog': 9,
            'murderous_root': 9
        },
        'thorns': {
            'ougloth_weak': 5,
            'ougloth': 14,
            'ougloth_brute': 6,
            'living_root': 3,
            'charencon': 3,
            'gob_dog': 9,
            'murderous_root': 10
        }
    }
    try:
        return tables[map_type]
    except:
        return None