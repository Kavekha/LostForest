import tcod as libtcod
from utils.death_functions import kill_player


class PlayerCompendium:
    player_archetype = {"player": {"base": "base_player"}}
    base_player_archetype = {
        "base_player": {
            "name": "Vagabond",
            "char": "@",
            "color": libtcod.white,
            "brain": None,
            "death_function": kill_player,
            "inventory": True,
            "hp": 30,
            "might": 3,
            "vitality": 3,
            "base_damage": (0, 2),
            "equipment": True,
        }
    }


def get_player_stats(type="player"):
    try:
        return PlayerCompendium.player_archetype[type]
    except:
        return None


def get_base_player_stats(type="base_player"):

    try:
        return PlayerCompendium.base_player_archetype[type]
    except:
        return None
