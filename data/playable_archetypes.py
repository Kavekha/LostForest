import libtcodpy as libtcod
from utils.death_functions import kill_player


class PlayerCompendium:
    player_archetype = {
        'player': {
            'base': 'base_player'
        }
    }
    base_player_archetype = {
        'base_player': {
            'char': '@',
            'color': libtcod.white,
            'brain': None,
            'death_function': kill_player,
            'inventory': True,
            'hp': 100,
            'might': 3,
            'vitality': 3
        }
    }


def get_player_stats(type='player'):
    try:
        return PlayerCompendium.player_archetype[type]
    except:
        return None


def get_base_player_stats(type='base_player'):

    try:
        return PlayerCompendium.base_player_archetype[type]
    except:
        return None
