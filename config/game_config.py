import tcod as libtcod

from utils.death_functions import kill_monster
from components.ai import BasicMonster

# XP SYSTEM
LEVEL_UP_BASE = 100
LEVEL_UP_FACTOR = 75
HP_GAIN_AT_LEVEL__UP = 3
AVAILABLE_STAT_INCREASE_PER_LEVEL = 1


# MOB XP VALUE
MIGHT_XP_VALUE = 1
DEXTERITY_XP_VALUE = 0.5
VITALITY_XP_VALUE = 0.5
HP_XP_VALUE = 0.5
BASE_DAMAGE_XP_VALUE = 1.5
XP_GLOBAL_MODIFIER = 0.2       # Modificateur sur formule globale, pour nerfer ou renforcer plus facilement.


# HIT FORMULA
BASE_HIT_CHANCE = 70
MODIFIER_HIT_CHANCE = 2.5   # Multiplie la difference de Dex entre les adversaires.
MIN_HIT_CHANCE = 10
MAX_HIT_CHANCE = 100
TO_HIT_ROLL = 100


# DAMAGE FORMULA
FINAL_DAMAGE_MODIFIER = 0.3  # Modificateur sur la formule totale, pour nerfer ou renforcer plus facilement.


# DEFAULT CREATURE STATS if not found.
DEFAULT_NAME = 'Unknown'
DEFAULT_APPEARANCE = '?'
DEFAULT_COLOR = libtcod.red
DEFAULT_CREATURE_BRAIN = BasicMonster

# DEFAULT FIGHTER COMPONENT STATS if not found
DEFAULT_FIGHTER_HP = 30
DEFAULT_FIGHTER_MIGHT = 3
DEFAULT_FIGHTER_DEXTERITY = 3
DEFAULT_FIGHTER_VITALITY = 3
DEFAULT_FIGHTER_DEATH_FUNCTION = kill_monster
DEFAULT_FIGHTER_BASE_DMG_MIN = 0
DEFAULT_FIGHTER_BASE_DMG_MAX = 2



