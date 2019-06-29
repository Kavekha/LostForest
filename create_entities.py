import tcod as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.equipment import Equipment
from components.equippable import Equippable, EquipmentSlot
from components.item import Item
from entities import Entity
from render_engine import RenderOrder
from components.ai import BasicMonster, Brainless
from components.level import Level
from config import game_config
from data_loaders.compendium import Compendium
from utils.death_functions import kill_player
from systems.target_selection import TargetType
from utils.effect_functions import heal, acide


def get_brain(brain):
    brain = brain.lower()

    brains = {
        'basicmonster': BasicMonster(),
        'brainless': Brainless()
    }

    return brains.get(brain, Brainless())


def get_target_type(target_type):
    if not target_type:
        return None

    target_type = target_type.lower()

    targets = {
        'self': TargetType.SELF,
        'fighting_entity': TargetType.FIGHTING_ENTITY,
        'item_entity': TargetType.ITEM_ENTITY,
        'other_entity': TargetType.OTHER_ENTITY,
        'tile': TargetType.TILE
    }

    return targets.get(target_type, TargetType.NONE)


def get_use_function(use_function):
    if not use_function:
        return None
    use_function = use_function.lower()

    functions = {
        'heal': heal,
        'acide': acide
    }

    return functions.get(use_function, None)


def create_entity(game, base_stats, entity_stats):
    if not entity_stats:
        entity_stats = base_stats

    name = entity_stats.get('name', base_stats.get('name', game_config.DEFAULT_NAME))
    appearance = entity_stats.get('char', base_stats.get('char', game_config.DEFAULT_APPEARANCE))
    color = entity_stats.get('color', base_stats.get('color', game_config.DEFAULT_COLOR))

    entity = Entity(game, 0, 0,
                    appearance, color, name)

    return entity


def create_fighter_component(base_stats, entity_stats):
    hp = entity_stats.get('hp', base_stats.get('hp', game_config.DEFAULT_FIGHTER_HP))
    might = entity_stats.get('might', base_stats.get('might', game_config.DEFAULT_FIGHTER_MIGHT))
    dexterity = entity_stats.get('dexterity', base_stats.get('dexterity', game_config.DEFAULT_FIGHTER_DEXTERITY))
    vitality = entity_stats.get('vitality', base_stats.get('vitality', game_config.DEFAULT_FIGHTER_VITALITY))
    death_function = entity_stats.get('death_function', base_stats.get('death_function', game_config.DEFAULT_FIGHTER_DEATH_FUNCTION))
    base_dmg_min = entity_stats.get('base_damage_min', base_stats.get('base_damage_min', game_config.DEFAULT_FIGHTER_BASE_DMG_MIN))
    base_dmg_max = entity_stats.get('base_damage_max', base_stats.get('base_damage_max', game_config.DEFAULT_FIGHTER_BASE_DMG_MAX))

    fighter_component = Fighter(hp=int(hp), might=int(might), dexterity=int(dexterity), vitality=int(vitality),
                                death_function=death_function,
                                base_dmg=(int(base_dmg_min), int(base_dmg_max)))

    return fighter_component


def create_ai_component(base_stats, entity_stats):
    brain = entity_stats.get('brain', base_stats.get('brain', game_config.DEFAULT_CREATURE_BRAIN))
    ai_component = get_brain(brain)

    return ai_component


def create_item_component(entity_stats):
    use_function = get_use_function(entity_stats.get('use_function', None))
    power = int(entity_stats.get('power', 0))
    target_type = get_target_type(entity_stats.get('target_type'))

    return Item(use_function, power, target_type)


def get_equippable_slot(slot):
    print(f'slot requested was {slot}')
    if not slot:
        return None

    slot = slot.lower()
    slots = {
        'main_hand': EquipmentSlot.MAIN_HAND,
        'off_hand': EquipmentSlot.OFF_HAND,
        'neck': EquipmentSlot.NECK,
        'chest': EquipmentSlot.CHEST
    }
    print(f'slot about to be return is {slots.get(slot, EquipmentSlot.NONE)}')
    return slots.get(slot, EquipmentSlot.NONE)


def create_equippable_component(entity_stats):

    equippable = entity_stats.get('equippable', False)
    print(f'equippable is {equippable}')

    if not equippable:
        return None

    equippable_slot = get_equippable_slot(entity_stats.get("slot", None))
    equippable_weapon_dmg_min = int(entity_stats.get("weapon_dmg_min", 0))
    equippable_weapon_dmg_max = int(entity_stats.get('weapon_dmg_max', 2))
    equippable_dmg_bonus = int(entity_stats.get("physical_power_bonus", 0))
    equippable_might_bonus = int(entity_stats.get("might_bonus", 0))
    equippable_hp_bonus = int(entity_stats.get("hp_bonus", 0))
    equippable_vitality_bonus = int(entity_stats.get("vitality_bonus", 0))
    equippable_dexterity_bonus = int(entity_stats.get('dexterity_bonus', 0))
    equippable_armor_bonus = int(entity_stats.get('armor_bonus', 0))

    equippable_component = Equippable(
        equippable_slot,
        weapon_damage=(equippable_weapon_dmg_min, equippable_weapon_dmg_max),
        physical_power_bonus=equippable_dmg_bonus,
        might_bonus=equippable_might_bonus,
        hp_bonus=equippable_hp_bonus,
        vitality_bonus=equippable_vitality_bonus,
        dexterity_bonus=equippable_dexterity_bonus,
        armor_bonus=equippable_armor_bonus
    )

    return equippable_component


def add_ego_attributes(item, defname):
    ego_attributes = Compendium.get_egos(defname)

    if not ego_attributes:
        return False

    try:
        item.equippable.physical_power_bonus += int(ego_attributes.get('physical_power', 0))
        item.equippable.might_bonus += int(ego_attributes.get('might', 0))
        item.equippable.hp_bonus += int(ego_attributes.get('hp', 0))
        item.equippable.vitality_bonus += int(ego_attributes.get('vitality', 0))
        item.equippable.dexterity_bonus += int(ego_attributes.get('dexterity', 0))
        item.equippable.armor_bonus += int(ego_attributes.get('armor', 0))
        item.name = item.name + ' ' + ego_attributes.get('name')
    except AttributeError:
        return False


def create_entity_item(game, item_defname, x, y):
    print(f'entity item requested : {item_defname}')
    entity_stats = Compendium.get_item(item_defname)

    if not entity_stats:
        return False

    print(f'entity state of {item_defname} is {entity_stats}')

    # we create the entity
    entity = create_entity(game, entity_stats, {})
    entity.blocks = False
    entity.render_order = RenderOrder.ITEM
    entity.x, entity.y = x, y

    item_component = create_item_component(entity_stats)
    entity.add_component(item_component, 'item')

    equippable_component = create_equippable_component(entity_stats)
    if equippable_component:
        entity.add_component(equippable_component, 'equippable')

    print(f"created item is {entity.name}, and equipable is {entity.equippable} ")
    if entity.equippable:
        print(f'slot equipement is {entity.equippable.slot}')

    return entity


def create_fighting_entity(game, entity_defname, x, y, player=False):
    # we get the entity stats from the defname
    entity_stats = Compendium.get_monster(entity_defname)

    # we get the base of the creature
    if entity_stats:
        base = entity_stats.get("base")
    else:
        entity_stats = {}
        base = entity_defname

    base_stats = Compendium.get_base_monster(base)

    if not base_stats:
        base_stats = {}

    if not base_stats and not entity_stats:
        return False

    # we create the entity
    entity = create_entity(game, base_stats, entity_stats)
    entity.blocks = True
    entity.render_order = RenderOrder.ACTOR
    entity.x, entity.y = x, y

    # we create fighting component
    fighter_component = create_fighter_component(base_stats, entity_stats)
    entity.add_component(fighter_component, 'fighter')

    # we create brain component
    ai_component = create_ai_component(base_stats, entity_stats)
    entity.add_component(ai_component, 'ai')

    # We calculate xp value
    xp_value = calculate_xp_value(entity.fighter)
    entity.fighter.xp_value = xp_value

    if player:
        equipment_component = Equipment()
        entity.add_component(equipment_component, 'equipment')

        inventory_component = Inventory(26)
        entity.add_component(inventory_component, 'inventory')

        level_component = Level()
        entity.add_component(level_component, 'level')

        entity.fighter.death_function = kill_player

    return entity


def calculate_xp_value(fighter):
    if not fighter.owner.ai:
        return 0

    min_dmg, max_dmg = fighter.base_damage
    damage_value = (min_dmg + max_dmg) * game_config.BASE_DAMAGE_XP_VALUE
    might_value = fighter.might * game_config.MIGHT_XP_VALUE
    dexterity_value = fighter.dexterity * game_config.DEXTERITY_XP_VALUE
    vitality_value = fighter.vitality * game_config.VITALITY_XP_VALUE
    hp_value = fighter.max_hp * game_config.HP_XP_VALUE

    total_xp_value = might_value * vitality_value * hp_value * damage_value * dexterity_value
    total_xp_value *= game_config.XP_GLOBAL_MODIFIER
    total_xp_value = int(total_xp_value)

    print("Total xp value of {} is {}".format(fighter.owner.name, total_xp_value))
    return total_xp_value


def old_create_entity_item(game, item_defname, x, y, dict_attributes):
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
        equippable_dmg_bonus = equippable.get("physical_power_bonus", 0)
        equippable_might_bonus = equippable.get("might_bonus", 0)
        equippable_hp_bonus = equippable.get("hp_bonus", 0)
        equippable_vitality_bonus = equippable.get("vitality_bonus", 0)
        equippable_dexterity_bonus = equippable.get('dexterity_bonus', 0)
        equippable_armor_bonus = equippable.get('armor_bonus', 0)

        equippable_component = Equippable(
            equippable_slot,
            weapon_damage=equippable_weapon_dmg,
            physical_power_bonus=equippable_dmg_bonus,
            might_bonus=equippable_might_bonus,
            hp_bonus=equippable_hp_bonus,
            vitality_bonus=equippable_vitality_bonus,
            dexterity_bonus=equippable_dexterity_bonus,
            armor_bonus=equippable_armor_bonus
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
