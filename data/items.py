import libtcodpy as libtcod
from effect_functions import heal, acide
from components.equippable import EquipmentSlot
from systems.target_selection import TargetType


def get_item_attributes(item):
    item_compendium = {
        'healing_potion': {
            'name': 'Potion de soins',
            'char': '!',
            'color': libtcod.violet,
            'use_function': heal,
            'power': 8,
            'target': TargetType.SELF
        },
        'acid_potion': {
            'name': 'Potion d acide',
            'char': '!',
            'color': libtcod.violet,
            'use_function': acide,
            'power': 8,
            'target': TargetType.FIGHTING_ENTITY
        },
        'staff': {
            'name': 'Baton de voyageur',
            'char': '/',
            'color': libtcod.white,
            'equippable': {
                'slot': EquipmentSlot.MAIN_HAND,
                'weapon_damage': (1, 4)
            }
        },
        'staff_force': {
            'name': 'Baton de voyageur',
            'char': '/',
            'color': libtcod.white,
            'equippable': {
                'slot': EquipmentSlot.MAIN_HAND,
                'weapon_damage': (1, 4),
                'damage_bonus': 1
            }
        },
        'bracelet': {
            'name': 'Bracelet de force',
            'char': 'o',
            'color': libtcod.white,
            'equippable': {
                'slot': EquipmentSlot.OFF_HAND,
                'might_bonus': 1
            }
        },
        'talisman': {
            'name': 'Talisman de vie',
            'char': 'v',
            'color': libtcod.white,
            'equippable': {
                'slot': EquipmentSlot.NECK,
                'hp_bonus': 5
            }
        },
        'robe': {
            'name': 'Robe de vitalite',
            'char': 'm',
            'color': libtcod.white,
            'equippable': {
                'slot': EquipmentSlot.CHEST,
                'vitality_bonus': 1
            }
        }
    }
    try:
        return item_compendium[item]
    except:
        return None
