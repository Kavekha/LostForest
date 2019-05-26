import libtcodpy as libtcod

from states.game_states import GameStates
from render_engine import RenderOrder
from config.constants import ConstColors


def become_corpse(entity, npc_killed=True):
    entity.char = '%'
    entity.color = libtcod.dark_red
    if npc_killed:
        entity.render_order = RenderOrder.CORPSE
        entity.blocks = False
        entity.fighter = None
        entity.ai = None
        entity.name = 'remains of ' + entity.name


def kill_player(player, attacker, events):
    become_corpse(player, npc_killed=False)
    events.add_event({'message': 'You died!',
                      'color': ConstColors.YOU_ARE_DEAD})
    events.add_event({'change_state': GameStates.PLAYER_DEAD})


def kill_monster(monster, attacker, events):
    events.add_event({'message': '{0} is dead!'.format(monster.name.capitalize()),
                      'color': ConstColors.HOSTILE_KILLED})
    become_corpse(monster)
