import libtcodpy as libtcod


def get_item_attributes(item):
    item_compendium = {
        'healing potion': {
            'char': '!',
            'color': libtcod.violet
        }
    }
    try:
        return item_compendium[item]
    except:
        return None
