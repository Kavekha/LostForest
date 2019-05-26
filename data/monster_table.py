def get_monster_table(map_type):
    tables = {
        'standard_map': {
            'Ougloth': 10,
            'Living root': 3
        },
        'forest_map': {
            'Ougloth': 10,
            'Living root': 3
        },
        'old_forest': {
            'Ougloth': 10,
            'Living root': 3
        },
        'thorns': {
            'Ougloth': 10,
            'Living root': 3
        }
    }
    try:
        return tables[map_type]
    except:
        return None