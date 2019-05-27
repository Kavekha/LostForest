import libtcodpy as libtcod
from components.fighter import Fighter
from components.inventory import Inventory
from components.item import Item
from utils.death_functions import kill_monster
from data.monsters import get_base_monster_stats, get_monster_stats
from data.playable_archetypes import get_player_stats, get_base_player_stats
from entities import Entity
from render_engine import RenderOrder


def create_fighting_entity(game, entity_name, x, y, player=False):
    print('create fighting entity : ', entity_name, x, y, player)
    if not player:
        entity_stats = get_monster_stats(entity_name)
    else:
        entity_stats = get_player_stats(entity_name)
    print('entity stats:', entity_stats)
    base = entity_stats.get('base')
    if not player:
        dict_stats = get_base_monster_stats(base)
    else:
        dict_stats = get_base_player_stats(base)
    print('base stats: ', dict_stats)

    entity_appearance = dict_stats.get('char', '?')
    entity_color = dict_stats.get('color', libtcod.red)
    inventory = dict_stats.get('inventory', False)
    death_function = dict_stats.get('death_function', kill_monster)
    entity_hp = dict_stats.get('hp', 10)
    entity_might = dict_stats.get('might', 3)
    entity_vitality = dict_stats.get('vitality', 3)
    ai_component = dict_stats.get('brain', None)

    if entity_stats.get('char'):
        entity_appearance = entity_stats.get('char')
    if entity_stats.get('color'):
        entity_color = entity_stats.get('color')
    if entity_stats.get('inventory'):
        inventory = entity_stats.get('inventory')
    if entity_stats.get('death_function'):
        death_function = entity_stats.get('death_function', kill_monster)
    if entity_stats.get('hp'):
        entity_hp += entity_stats.get('hp')
    if entity_stats.get('might'):
        entity_might += entity_stats.get('might')
    if entity_stats.get('vitality'):
        entity_vitality += entity_stats.get('vitality')
    if entity_stats.get('brain'):
        ai_component += entity_stats.get('brain')

    fighter_component = Fighter(hp=entity_hp, might=entity_might, vitality=entity_vitality,
                                death_function=death_function)
    if inventory:
        inventory_component = Inventory(26)
    else:
        inventory_component = None

    entity = Entity(game, x, y,
                    entity_appearance, entity_color, entity_name,
                    blocks=True,
                    fighter=fighter_component,
                    inventory=inventory_component,
                    ai=ai_component,
                    render_order=RenderOrder.ACTOR)
    print('ai component at end : ', entity.ai)
    return entity


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
