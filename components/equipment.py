from components.equippable import EquipmentSlot, get_equipment_in_slot
from systems.localization import Texts
from config import color_config


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, neck=None, chest=None):
        self.owner = None
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.neck = neck
        self.chest = chest

    def get_equipped_items_list(self):
        equipped_items = []
        if self.main_hand:
            equipped_items.append(self.main_hand)
        elif self.off_hand:
            equipped_items.append(self.off_hand)
        elif self.neck:
            equipped_items.append(self.neck)
        elif self.chest:
            equipped_items.append(self.chest)

        return equipped_items

    @property
    def weapon_damage(self):
        weapon_damage = None

        if self.main_hand and self.main_hand.equippable:
            weapon_damage = self.main_hand.equippable.weapon_damage

        return weapon_damage

    @property
    def physical_power_bonus(self):
        bonus = 0

        for equipment in [self.main_hand, self.off_hand, self.neck, self.chest]:
            if equipment and equipment.equippable:
                bonus += equipment.equippable.physical_power_bonus

        return bonus

    @property
    def might_bonus(self):
        bonus = 0

        for equipment in [self.main_hand, self.off_hand, self.neck, self.chest]:
            if equipment and equipment.equippable:
                bonus += equipment.equippable.might_bonus

        return bonus

    @property
    def hp_bonus(self):
        bonus = 0

        for equipment in [self.main_hand, self.off_hand, self.neck, self.chest]:
            if equipment and equipment.equippable:
                bonus += equipment.equippable.hp_bonus

        return bonus

    @property
    def vitality_bonus(self):
        bonus = 0

        for equipment in [self.main_hand, self.off_hand, self.neck, self.chest]:
            if equipment and equipment.equippable:
                bonus += equipment.equippable.vitality_bonus

        return bonus

    @property
    def dexterity_bonus(self):
        bonus = 0

        for equipment in [self.main_hand, self.off_hand, self.neck, self.chest]:
            if equipment and equipment.equippable:
                bonus += equipment.equippable.dexterity_bonus

        return bonus

    @property
    def armor_bonus(self):
        bonus = 0

        for equipment in [self.main_hand, self.off_hand, self.neck, self.chest]:
            if equipment and equipment.equippable:
                bonus += equipment.equippable.armor_bonus

        return bonus

    def set_equipment_in_slot(self, slot, equippable_entity):
        if slot == EquipmentSlot.MAIN_HAND:
            self.main_hand = equippable_entity
        elif slot == EquipmentSlot.OFF_HAND:
            self.off_hand = equippable_entity
        elif slot == EquipmentSlot.NECK:
            self.neck = equippable_entity
        elif slot == EquipmentSlot.CHEST:
            self.chest = equippable_entity

    def unequip_item(self, slot, entity_to_unequip):
        events = self.owner.game.events
        self.set_equipment_in_slot(slot, None)
        events.add_event(
            {
                "message": Texts.get_text('UNEQUIP_ITEM').format(entity_to_unequip.name),
                "color": color_config.UNEQUIP,
            }
        )

    def equip_item(self, slot, entity_to_equip):
        events = self.owner.game.events
        self.set_equipment_in_slot(slot, entity_to_equip)
        events.add_event(
            {
                "message": Texts.get_text('EQUIP_ITEM').format(entity_to_equip.name),
                "color": color_config.EQUIP,
            }
        )

    def toggle_equip(self, equippable_entity):
        equippable_slot = equippable_entity.equippable.slot
        equipment_in_slot = get_equipment_in_slot(equippable_slot, self)

        # Sur le slot de l'item que j'utilise : j'ai deja l'item je desequipe.
        if equipment_in_slot == equippable_entity:
            self.unequip_item(equippable_slot, equippable_entity)
        else:
            # J ai deja un item, je le desequipe.
            if equipment_in_slot:
                self.unequip_item(equippable_slot, equipment_in_slot)
            self.equip_item(equippable_slot, equippable_entity)
