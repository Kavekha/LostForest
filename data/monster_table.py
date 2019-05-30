def get_monster_table(map_type):
    tables = {
        'standard_map': {
            'ougloth': 10,
            'living root': 3
        },
        'forest_map': {
            'ougloth_weak': 10,
            'ougloth': 15,
            'ougloth_brute': 5,
            'living root': 10
        },
        'old_forest': {
            'ougloth_weak': 7,
            'ougloth': 14,
            'ougloth_brute': 8,
            'living root': 10
        },
        'thorns': {
            'ougloth_weak': 5,
            'ougloth': 12,
            'ougloth_brute': 12,
            'living root': 10
        }
    }
    try:
        return tables[map_type]
    except:
        return None