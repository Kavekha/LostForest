from enum import Enum
from config.constants import ConstTexts


class EquipmentSlot(Enum):
    NONE = 0
    MAIN_HAND = 1
    OFF_HAND = 2
    NECK = 3
    CHEST = 4


def get_equipment_in_slot(slot, entity_equipement):
    if slot == EquipmentSlot.MAIN_HAND:
        return entity_equipement.main_hand
    elif slot == EquipmentSlot.OFF_HAND:
        return entity_equipement.off_hand
    elif slot == EquipmentSlot.NECK:
        return entity_equipement.neck
    elif slot == EquipmentSlot.CHEST:
        return entity_equipement.chest


def slot_to_text(slot):
    if slot == EquipmentSlot.MAIN_HAND:
        return ConstTexts.EQUIPMENT_SLOT_MAIN_HAND
    elif slot == EquipmentSlot.OFF_HAND:
        return ConstTexts.EQUIPMENT_SLOT_OFF_HAND
    elif slot == EquipmentSlot.NECK:
        return ConstTexts.EQUIPMENT_SLOT_NECK
    elif slot == EquipmentSlot.CHEST:
        return ConstTexts.EQUIPMENT_SLOT_CHEST
    return ConstTexts.EQUIPMENT_SLOT_NONE


class Equippable:
    def __init__(
        self,
        slot,
        weapon_damage=(0, 2),
        damage_bonus=0,
        might_bonus=0,
        hp_bonus=0,
        vitality_bonus=0,
    ):
        self.slot = slot
        self.weapon_damage = weapon_damage
        self.damage_bonus = damage_bonus
        self.might_bonus = might_bonus
        self.hp_bonus = hp_bonus
        self.vitality_bonus = vitality_bonus
