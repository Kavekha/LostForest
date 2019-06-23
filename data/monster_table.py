from config import map_gen_config


def get_monster_table(map_type):

    tables = {
        "standard_map": {
            "ougloth_pack": map_gen_config.FREQUENCY_RARE,
            "root_pack": map_gen_config.FREQUENCY_RARE,
            "gob_dog": map_gen_config.FREQUENCY_UNCOMMON
         },

        "forest_map": {
            "ougloth_recon_tiers1": map_gen_config.FREQUENCY_RARE,
            "root_pack_tiers1": map_gen_config.FREQUENCY_UNCOMMON,
            "various_beasts_tiers1": map_gen_config.FREQUENCY_COMMON
        },

        "various_beasts_tiers1": {
            "gob_dog": map_gen_config.FREQUENCY_UNCOMMON,
        },

        'ougloth_recon_tiers1': {
            "ougloth_weak": map_gen_config.FREQUENCY_UNCOMMON,
            "ougloth": map_gen_config.FREQUENCY_RARE,
        },

        'root_pack_tiers1': {
            "living_root": map_gen_config.FREQUENCY_VERY_COMMON,
            "murderous_root": map_gen_config.FREQUENCY_VERY_RARE
        },

        'ougloth_pack': {
            "ougloth_weak": map_gen_config.FREQUENCY_UNCOMMON,
            "ougloth": map_gen_config.FREQUENCY_UNCOMMON,
            "ougloth_brute": map_gen_config.FREQUENCY_RARE
        },
        'root_pack': {
            "living_root": map_gen_config.FREQUENCY_COMMON,
            "murderous_root": map_gen_config.FREQUENCY_RARE
        },


        "old_forest": {
            "ougloth_recon_tiers2": map_gen_config.FREQUENCY_UNCOMMON,
            "root_pack_tiers2": map_gen_config.FREQUENCY_RARE,
            "various_beasts_tiers2": map_gen_config.FREQUENCY_UNCOMMON
        },

        "various_beasts_tiers2": {
            "gob_dog": map_gen_config.FREQUENCY_COMMON,
            "charencon": map_gen_config.FREQUENCY_VERY_RARE

        },

        'ougloth_recon_tiers2': {
            "ougloth_weak": map_gen_config.FREQUENCY_RARE,
            "ougloth": map_gen_config.FREQUENCY_COMMON,
            "ougloth_brute": map_gen_config.FREQUENCY_RARE
        },

        'root_pack_tiers2': {
            "living_root": map_gen_config.FREQUENCY_UNCOMMON,
            "murderous_root": map_gen_config.FREQUENCY_UNCOMMON
        },

        "thorns": {
            "ougloth_recon_tiers3": map_gen_config.FREQUENCY_UNCOMMON,
            "root_pack_tiers3": map_gen_config.FREQUENCY_COMMON,
            "various_beasts_tiers3": map_gen_config.FREQUENCY_UNCOMMON
        },

        "various_beasts_tiers3": {
            "gob_dog": map_gen_config.FREQUENCY_RARE,
            "charencon": map_gen_config.FREQUENCY_UNCOMMON

        },

        'ougloth_recon_tiers3': {
            "ougloth_weak": map_gen_config.FREQUENCY_VERY_RARE,
            "ougloth": map_gen_config.FREQUENCY_COMMON,
            "ougloth_brute": map_gen_config.FREQUENCY_UNCOMMON
        },

        'root_pack_tiers3': {
            "living_root": map_gen_config.FREQUENCY_UNCOMMON,
            "murderous_root": map_gen_config.FREQUENCY_UNCOMMON,
            "tertre_errant": map_gen_config.FREQUENCY_RARE
        },
    }
    try:
        return tables[map_type]
    except:
        return None
