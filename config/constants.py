import libtcodpy as libtcod


class ConstColors:
    # Info
    NEUTRAL_INFO_COLOR = libtcod.white
    IMPORTANT_INFO_COLOR = libtcod.yellow
    POSITIVE_INFO_COLOR = libtcod.light_blue
    # Fighting info
    YOU_ARE_DEAD = libtcod.red
    HOSTILE_KILLED = libtcod.orange
    DAMAGING_ATTACK = libtcod.white
    NO_DAMAGE_ATTACK = libtcod.white
    # collection
    ITEM_PICKED = libtcod.light_blue
    INVENTORY_FULL = libtcod.yellow
    NOTHING_TO_PICK_UP = libtcod.yellow
    CANNOT_BE_USED = libtcod.orange
    # Health
    FULL_HEAL_ALREADY = libtcod.yellow
    WOUND_HEALED = libtcod.green
    REST_AFTER_STAIRS_COLOR = libtcod.light_violet
