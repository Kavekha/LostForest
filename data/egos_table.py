from config import map_gen_config


def get_ego_table(map_type):
    tables = {
        "standard_map": {
            "ego_might": map_gen_config.FREQUENCY_RARE,
            "ego_dexterity": map_gen_config.FREQUENCY_RARE,
            "ego_vitality": map_gen_config.FREQUENCY_RARE,
            "ego_hp": map_gen_config.FREQUENCY_RARE,
            "ego_armor": map_gen_config.FREQUENCY_RARE
        },
        "forest_map": {
            "ego_might": map_gen_config.FREQUENCY_RARE,
            "ego_dexterity": map_gen_config.FREQUENCY_RARE,
            "ego_vitality": map_gen_config.FREQUENCY_RARE,
            "ego_hp": map_gen_config.FREQUENCY_RARE,
            "ego_armor": map_gen_config.FREQUENCY_RARE
        },
        "old_forest": {
            "ego_might": map_gen_config.FREQUENCY_RARE,
            "ego_dexterity": map_gen_config.FREQUENCY_RARE,
            "ego_vitality": map_gen_config.FREQUENCY_RARE,
            "ego_hp": map_gen_config.FREQUENCY_RARE,
            "ego_armor": map_gen_config.FREQUENCY_RARE
        },
        "thorns": {
            "ego_might": map_gen_config.FREQUENCY_RARE,
            "ego_dexterity": map_gen_config.FREQUENCY_RARE,
            "ego_vitality": map_gen_config.FREQUENCY_RARE,
            "ego_hp": map_gen_config.FREQUENCY_RARE,
            "ego_armor": map_gen_config.FREQUENCY_RARE
        }
    }
    try:
        print(f'egos table is : {tables[map_type]}')
        return tables[map_type]
    except:
        return None
