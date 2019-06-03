def get_item_table(map_type):
    tables = {
        'standard_map': {
            'healing_potion': 16,
            'staff': 10,
            'bracelet': 5,
            'staff_force': 3,
            'talisman': 5,
            'robe': 8
        },
        'forest_map': {
            'healing_potion': 32,
            'staff': 10,
            'bracelet': 5,
            'staff_force': 3,
            'talisman': 5,
            'robe': 8,
            'acid_potion': 10
        },
        'old_forest': {
            'healing_potion': 34,
            'staff': 5,
            'bracelet': 8,
            'staff_force': 5,
            'talisman': 8,
            'robe': 6,
            'acid_potion': 12
        },
        'thorns': {
            'healing_potion': 40,
            'staff': 2,
            'bracelet': 6,
            'staff_force': 10,
            'talisman': 6,
            'robe': 9,
            'acid_potion': 14
        }
    }
    try:
        return tables[map_type]
    except:
        return None
