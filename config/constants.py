import libtcodpy as libtcod


class ConstLevel:
    LEVEL_UP_BASE = 200
    LEVEL_UP_FACTOR = 150
    MIGHT_XP_VALUE = 0.5
    VITALITY_XP_VALUE = 0.75
    HP_XP_VALUE = 0.25
    BASE_DAMAGE_XP_VALUE = 1
    AVAILABLE_STAT_INCREASE_PER_LEVEL = 1


class ConstColors:
    # Info
    NEUTRAL_INFO_COLOR = libtcod.white
    IMPORTANT_INFO_COLOR = libtcod.yellow
    POSITIVE_INFO_COLOR = libtcod.lighter_blue
    # Fighting info
    YOU_ARE_DEAD = libtcod.red
    HOSTILE_KILLED = libtcod.orange
    DAMAGING_ATTACK = libtcod.white
    NO_DAMAGE_ATTACK = libtcod.grey
    # collection
    ITEM_PICKED = libtcod.light_blue
    INVENTORY_FULL = libtcod.yellow
    NOTHING_TO_PICK_UP = libtcod.yellow
    CANNOT_BE_USED = libtcod.orange
    # Health
    FULL_HEAL_ALREADY = libtcod.yellow
    WOUND_HEALED = libtcod.green
    REST_AFTER_STAIRS_COLOR = libtcod.light_violet


class ConstTexts:
    # travel
    NO_STAIRS_THERE = 'There are no stairs here.'
    REST_AFTER_STAIRS = 'You take a moment to rest, and recover your strength.'
    # health
    FULL_HEAL_ALREADY = 'You are already at full health'
    WOUND_HEALED = 'Your wounds start to feel better!'
    # inventory & items / collections
    INVENTORY_FULL = 'You cannot carry any more, your inventory is full'
    NOTHING_TO_PICK_UP = 'There is nothing here to pick up.'
    INVENTORY_EMPTY = 'inventory is empty'
    INVENTORY_HEADER = 'Press the key next to an item to use it, or Esc to cancel.\n'
    # victory
    VICTORY_LAST_FLOOR_BASIC = 'OUT OF DANGER!! You escape the Cursed Forest!'
    # XP
    LEVEL_UP = 'You reach level {} ! You feel powerfull.'
    LEVEL_UP_MENU_HEADER = 'Choose which stat you want to increase. \n Available : {}.'

