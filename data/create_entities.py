import libtcodpy as libtcod
from components.fighter import Fighter
from components.inventory import Inventory
from components.item import Item
from utils.death_functions import kill_monster
from data.monsters import get_base_monster_stats, get_monster_stats
from data.playable_archetypes import get_player_stats, get_base_player_stats
from entities import Entity
from render_engine import RenderOrder
from components.ai import BasicMonster, Brainless
from components.level import Level
from config.constants import ConstLevel


def get_brain(brain):
    if brain == 'BasicMonster':
        return BasicMonster()
    elif brain == 'Brainless':
        return Brainless()
    else:
        return None


def create_fighting_entity(game, entity_defname, x, y, player=False):
    if not player:
        entity_stats = get_monster_stats(entity_defname)
    else:
        entity_stats = get_player_stats(entity_defname)
    base = entity_stats.get('base')
    if not player:
        dict_stats = get_base_monster_stats(base)
    else:
        dict_stats = get_base_player_stats(base)

    entity_name = dict_stats.get('name', 'Unknown')
    entity_appearance = dict_stats.get('char', '?')
    entity_color = dict_stats.get('color', libtcod.red)
    inventory = dict_stats.get('inventory', False)
    death_function = dict_stats.get('death_function', kill_monster)
    entity_base_dmg = dict_stats.get('base_damage', (0, 2))
    entity_hp = dict_stats.get('hp', 10)
    entity_might = dict_stats.get('might', 3)
    entity_vitality = dict_stats.get('vitality', 3)
    ai_component = get_brain(dict_stats.get('brain', None))

    if entity_stats.get('name'):
        entity_name = entity_stats.get('name')
    if entity_stats.get('char'):
        entity_appearance = entity_stats.get('char')
    if entity_stats.get('color'):
        entity_color = entity_stats.get('color')
    if entity_stats.get('inventory'):
        inventory = entity_stats.get('inventory')
    if entity_stats.get('death_function'):
        death_function = entity_stats.get('death_function', kill_monster)
    if entity_stats.get('base_damage'):
        entity_base_dmg = entity_stats.get('base_damage')
    if entity_stats.get('hp'):
        entity_hp = entity_stats.get('hp')
    if entity_stats.get('might'):
        entity_might = entity_stats.get('might')
    if entity_stats.get('vitality'):
        entity_vitality = entity_stats.get('vitality')
    if entity_stats.get('brain'):
        ai_component = get_brain(entity_stats.get('brain'))

    fighter_component = Fighter(hp=entity_hp, might=entity_might, vitality=entity_vitality,
                                death_function=death_function, base_dmg=entity_base_dmg)
    if inventory:
        inventory_component = Inventory(26)
    else:
        inventory_component = None

    if player:
        level_component = Level()
    else:
        level_component = None

    entity = Entity(game, x, y,
                    entity_appearance, entity_color, entity_name,
                    blocks=True,
                    fighter=fighter_component,
                    inventory=inventory_component,
                    ai=ai_component,
                    level=level_component,
                    render_order=RenderOrder.ACTOR)

    xp_value = calculate_xp_value(entity.fighter)
    entity.fighter.xp_value = xp_value

    return entity


def calculate_xp_value(fighter):
    if not fighter.owner.ai:
        return 0

    min_dmg, max_dmg = fighter.base_damage
    damage_value = min_dmg + max_dmg * ConstLevel.BASE_DAMAGE_XP_VALUE
    might_value = fighter.might * ConstLevel.MIGHT_XP_VALUE
    vitality_value = fighter.vitality * ConstLevel.VITALITY_XP_VALUE

    hp_value = fighter.max_hp * ConstLevel.HP_XP_VALUE

    total_xp_value = might_value * vitality_value * hp_value * damage_value
    total_xp_value = int(total_xp_value)

    print('Total xp value of {} is {}'.format(fighter.owner.name, total_xp_value))
    return total_xp_value


def create_entity_item(game, item_name, x, y, dict_attributes):
    appearance = dict_attributes.get('char', '?')
    color = dict_attributes.get('color', libtcod.red)
    use_function = dict_attributes.get('use_function', None)
    power = dict_attributes.get('power', 0)

    item_component = Item(use_function=use_function, power=power)
    item = Entity(game, x, y,
                  appearance, color, item_name,
                  item=item_component,
                  render_order=RenderOrder.ITEM)
    return item
