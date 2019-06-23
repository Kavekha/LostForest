from config import map_gen_config


def get_item_table(map_type):
    tables = {
        "standard_map": {
            "potions": map_gen_config.FREQUENCY_VERY_COMMON,
            "weapons": map_gen_config.FREQUENCY_VERY_RARE,
            "jewels": map_gen_config.FREQUENCY_RARE,
            "armors": map_gen_config.FREQUENCY_VERY_RARE
        },
        "forest_map": {
            "potions": map_gen_config.FREQUENCY_VERY_COMMON,
            "weapons": map_gen_config.FREQUENCY_VERY_RARE,
            "jewels": map_gen_config.FREQUENCY_RARE,
            "armors": map_gen_config.FREQUENCY_VERY_RARE
        },
        "old_forest": {
            "potions": map_gen_config.FREQUENCY_VERY_COMMON,
            "weapons": map_gen_config.FREQUENCY_VERY_RARE,
            "jewels": map_gen_config.FREQUENCY_RARE,
            "armors": map_gen_config.FREQUENCY_VERY_RARE
        },
        "thorns": {
            "potions": map_gen_config.FREQUENCY_VERY_COMMON,
            "weapons": map_gen_config.FREQUENCY_VERY_RARE,
            "jewels": map_gen_config.FREQUENCY_RARE,
            "armors": map_gen_config.FREQUENCY_VERY_RARE
        },
        "potions": {
            "healing_potion": map_gen_config.FREQUENCY_VERY_COMMON,
            "acid_potion": map_gen_config.FREQUENCY_UNCOMMON
        },
        "weapons": {
            "staff": map_gen_config.FREQUENCY_COMMON,
            "staff_force": map_gen_config.FREQUENCY_RARE
        },
        "jewels": {
            "bracelet": map_gen_config.FREQUENCY_UNCOMMON,
            "talisman": map_gen_config.FREQUENCY_UNCOMMON
        },
        "armors": {
            "robe": map_gen_config.FREQUENCY_UNCOMMON
        }
    }
    try:
        return tables[map_type]
    except:
        return None


'''
        "forest_map": {
            "healing_potion": 21,
            "staff": 6,
            "bracelet": 7,
            "staff_force": 2,
            "talisman": 7,
            "robe": 7,
            "acid_potion": 10,
        },
        '''