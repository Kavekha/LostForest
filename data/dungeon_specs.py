def get_dungeon_config(dungeon_name="dungeon"):
    config = {
        "dungeon": {"max_floor": 10},
        "Foret eternelle": {
            "max_floor": 5,
            "floors": {"1": "forest_map", "3": "old_forest", "5": "thorns"},
        },
    }
    return config[dungeon_name]
