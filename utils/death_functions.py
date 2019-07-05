import tcod as libtcod

from render_engine import RenderOrder
from config import color_config
from data_loaders.localization import Texts


def become_corpse(entity, npc_killed=True):
    entity.char = "%"
    entity.color = 'dark red'
    if npc_killed:
        entity.render_order = RenderOrder.CORPSE
        entity.blocks = False
        entity.fighter = None
        entity.ai = None
        entity.name = Texts.get_text('REMAINS_OF_SOMEONE') + entity.name


def kill_player(player, attacker, events):
    become_corpse(player, npc_killed=False)
    events.add_event({"message": Texts.get_text('YOU_DIED'), "color": color_config.YOU_ARE_DEAD})


def kill_monster(monster, attacker, events):
    events.add_event(
        {
            "message": Texts.get_text('CHAR_IS_DEAD').format(monster.name.capitalize()),
            "color": color_config.HOSTILE_KILLED,
        }
    )
    become_corpse(monster)
