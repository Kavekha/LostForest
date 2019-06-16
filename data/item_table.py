def get_item_table(map_type):
    tables = {
        "standard_map": {
            "healing_potion": 16,
            "staff": 10,
            "bracelet": 5,
            "staff_force": 3,
            "talisman": 5,
            "robe": 8,
        },
        "forest_map": {
            "healing_potion": 21,
            "staff": 6,
            "bracelet": 7,
            "staff_force": 2,
            "talisman": 7,
            "robe": 7,
            "acid_potion": 10,
        },
        "old_forest": {
            "healing_potion": 21,
            "staff": 6,
            "bracelet": 7,
            "staff_force": 2,
            "talisman": 7,
            "robe": 7,
            "acid_potion": 10,
        },
        "thorns": {
            "healing_potion": 21,
            "staff": 6,
            "bracelet": 7,
            "staff_force": 2,
            "talisman": 7,
            "robe": 7,
            "acid_potion": 10,
        },
    }
    try:
        return tables[map_type]
    except:
        return None
