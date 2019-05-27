import libtcodpy as libtcod
from components.ai import BasicMonster, Brainless


class MonsterCompendium:
    monster_compendium = {
        'ougloth': {
            'base': 'ougloth'
        },
        'ougloth_weak': {
            'base': 'ougloth',
            'color': libtcod.red,
            'hp': 7,
            'vitality': 2
        },
        'ougloth_brute': {
            'base': 'ougloth',
            'color': libtcod.dark_red,
            'hp': 14,
            'might': 4
        },
        'living root': {
            'base': 'root'
        }
    }


class BaseMonsterCompendium:
    base_monster_compendium = {
        'ougloth': {
            'char': 'o',
            'color': libtcod.desaturated_red,
            'brain': BasicMonster(),
            'hp': 10,
            'might': 2,
            'vitality': 3
        },
        'root': {
            'char': 'x',
            'color': libtcod.desaturated_red,
            'brain': Brainless(),
            'hp': 5,
            'might': 0,
            'vitality': 1
        }
    }


def get_monster_stats(monster):
    try:
        return MonsterCompendium.monster_compendium[monster]
    except:
        return None


def get_base_monster_stats(base_monster):
    try:
        return BaseMonsterCompendium.base_monster_compendium[base_monster]
    except:
        return None
