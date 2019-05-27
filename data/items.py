import libtcodpy as libtcod
from effect_functions import heal


def get_item_attributes(item):
    item_compendium = {
        'healing potion': {
            'char': '!',
            'color': libtcod.violet,
            'use_function': heal,
            'power': 4
        },
        'greater healing potion': {
            'char': '!',
            'color': libtcod.violet,
            'use_function': heal,
            'power': 12
        }

    }
    try:
        return item_compendium[item]
    except:
        return None
