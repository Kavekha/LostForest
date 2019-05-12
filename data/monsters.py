import libtcodpy as libtcod
from components.ai import BasicMonster, Brainless


def get_monster_stats(monster):
    monster_compendium = {
        'Ougloth': {
            'hp': 10,
            'char': 'o',
            'color': libtcod.desaturated_green,
            'brain': BasicMonster()
        },
        'Living root': {
            'hp': 5,
            'char': 'x',
            'color': libtcod.dark_green,
            'brain': Brainless()
        }
    }
    try:
        return monster_compendium[monster]
    except:
        return None