import tcod as libtcod
from components.fighter import Fighter
from components.inventory import Inventory
from components.equipment import Equipment
from components.equippable import Equippable, EquipmentSlot
from components.item import Item
from utils.death_functions import kill_monster
from data.monsters import get_base_monster_stats, get_monster_stats
from data.playable_archetypes import get_player_stats, get_base_player_stats
from entities import Entity
from render_engine import RenderOrder
from components.ai import BasicMonster, Brainless
from components.level import Level
from config import game_config


def get_brain(brain):
    if brain == "BasicMonster":
        return BasicMonster()
    elif brain == "Brainless":
        return Brainless()
    else:
        return None


def create_fighting_entity(game, entity_defname, x, y, player=False):
    if not player:
        entity_stats = get_monster_stats(entity_defname)
    else:
        entity_stats = get_player_stats(entity_defname)
    base = entity_stats.get("base")
    if not player:
        dict_stats = get_base_monster_stats(base)
    else:
        dict_stats = get_base_player_stats(base)

    entity_name = dict_stats.get("name", "Unknown")
    entity_appearance = dict_stats.get("char", "?")
    entity_color = dict_stats.get("color", libtcod.red)
    inventory = dict_stats.get("inventory", False)
    equipment = dict_stats.get("equipment", False)
    death_function = dict_stats.get("death_function", kill_monster)
    entity_base_dmg = dict_stats.get("base_damage", (0, 2))
    entity_hp = dict_stats.get("hp", 10)
    entity_might = dict_stats.get("might", 3)
    entity_vitality = dict_stats.get("vitality", 3)
    ai_component = get_brain(dict_stats.get("brain", None))

    if entity_stats.get("name"):
        entity_name = entity_stats.get("name")
    if entity_stats.get("char"):
        entity_appearance = entity_stats.get("char")
    if entity_stats.get("color"):
        entity_color = entity_stats.get("color")
    if entity_stats.get("inventory"):
        inventory = entity_stats.get("inventory")
    if entity_stats.get("equipment"):
        equipment = entity_stats.get("equipment")
    if entity_stats.get("death_function"):
        death_function = entity_stats.get("death_function", kill_monster)
    if entity_stats.get("base_damage"):
        entity_base_dmg = entity_stats.get("base_damage")
    if entity_stats.get("hp"):
        entity_hp = entity_stats.get("hp")
    if entity_stats.get("might"):
        entity_might = entity_stats.get("might")
    if entity_stats.get("vitality"):
        entity_vitality = entity_stats.get("vitality")
    if entity_stats.get("brain"):
        ai_component = get_brain(entity_stats.get("brain"))

    fighter_component = Fighter(
        hp=entity_hp,
        might=entity_might,
        vitality=entity_vitality,
        death_function=death_function,
        base_dmg=entity_base_dmg,
    )
    if inventory:
        inventory_component = Inventory(26)
    else:
        inventory_component = None

    if equipment:
        equipment_component = Equipment()
    else:
        equipment_component = None

    if player:
        level_component = Level()
    else:
        level_component = None

    entity = Entity(
        game,
        x,
        y,
        entity_appearance,
        entity_color,
        entity_name,
        blocks=True,
        fighter=fighter_component,
        inventory=inventory_component,
        equipment=equipment_component,
        ai=ai_component,
        level=level_component,
        render_order=RenderOrder.ACTOR,
    )

    xp_value = calculate_xp_value(entity.fighter)
    entity.fighter.xp_value = xp_value

    return entity


def calculate_xp_value(fighter):
    if not fighter.owner.ai:
        return 0

    min_dmg, max_dmg = fighter.base_damage
    damage_value = min_dmg + max_dmg * game_config.BASE_DAMAGE_XP_VALUE
    might_value = fighter.might * game_config.MIGHT_XP_VALUE
    vitality_value = fighter.vitality * game_config.VITALITY_XP_VALUE

    hp_value = fighter.max_hp * game_config.HP_XP_VALUE

    total_xp_value = might_value * vitality_value * hp_value * damage_value
    total_xp_value = int(total_xp_value)

    print("Total xp value of {} is {}".format(fighter.owner.name, total_xp_value))
    return total_xp_value


def create_entity_item(game, item_defname, x, y, dict_attributes):
    name = dict_attributes.get("name", "?")
    appearance = dict_attributes.get("char", "?")
    color = dict_attributes.get("color", libtcod.red)
    use_function = dict_attributes.get("use_function", None)
    power = dict_attributes.get("power", 0)
    equippable = dict_attributes.get("equippable", False)
    target = dict_attributes.get("target", None)
    value = dict_attributes.get("value", 30)

    if equippable:
        equippable_slot = equippable.get("slot", EquipmentSlot.NONE)
        equippable_weapon_dmg = equippable.get("weapon_damage", (0, 2))
        equippable_dmg_bonus = equippable.get("damage_bonus", 0)
        equippable_might_bonus = equippable.get("might_bonus", 0)
        equippable_hp_bonus = equippable.get("hp_bonus", 0)
        equippable_vitality_bonus = equippable.get("vitality_bonus", 0)

        equippable_component = Equippable(
            equippable_slot,
            weapon_damage=equippable_weapon_dmg,
            damage_bonus=equippable_dmg_bonus,
            might_bonus=equippable_might_bonus,
            hp_bonus=equippable_hp_bonus,
            vitality_bonus=equippable_vitality_bonus,
        )
    else:
        equippable_component = None

    item_component = Item(
        use_function=use_function, power=power, target_type=target, value=value
    )
    item = Entity(
        game,
        x,
        y,
        appearance,
        color,
        name,
        item=item_component,
        equippable=equippable_component,
        render_order=RenderOrder.ITEM,
    )

    print("created item is {}, and equipable is {} ".format(item.name, item.equippable))
    return item
