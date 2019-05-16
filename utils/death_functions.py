import libtcodpy as libtcod

from states.game_states import GameStates
from render_engine import RenderOrder
from game_messages import Message


def become_corpse(entity):
    entity.char = '%'
    entity.color = libtcod.dark_red
    entity.render_order = RenderOrder.CORPSE


def kill_player(player):
    become_corpse(player)
    return 'You died!', GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())

    become_corpse(monster)

    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name

    return death_message