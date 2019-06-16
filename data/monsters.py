import tcod as libtcod


class MonsterCompendium:
    monster_compendium = {
        "ougloth": {"base": "ougloth"},
        "ougloth_weak": {
            "name": "Ougloth malingre",
            "base": "ougloth",
            "color": libtcod.desaturated_red,
            "hp": 7,
            "vitality": 2,
        },
        "ougloth_brute": {
            "name": "Brute Ougloth",
            "base": "ougloth",
            "color": libtcod.red,
            "hp": 14,
            "might": 5,
        },
        "living_root": {"name": "Racines vivantes", "base": "root"},
        "murderous_root": {
            "name": "Racines devorantes",
            "base": "root",
            "brain": "BasicMonster",
            "hp": 8,
            "might": 2,
            "vitality": 1,
            "base_damage": (0, 2),
        },
        "charencon": {"base": "charencon"},
        "gob_dog": {"base": "gob_dog"},
        "tertre_errant": {"base": "tertre_errant"},
    }


class BaseMonsterCompendium:
    base_monster_compendium = {
        "ougloth": {
            "name": "Ougloth",
            "char": "o",
            "color": libtcod.dark_red,
            "brain": "BasicMonster",
            "hp": 10,
            "might": 4,
            "vitality": 3,
            "base_damage": (0, 2),
        },
        "root": {
            "name": "Racines",
            "char": "x",
            "color": libtcod.desaturated_red,
            "brain": "Brainless",
            "hp": 5,
            "might": 0,
            "vitality": 1,
        },
        # Coleoptere geant.
        "charencon": {
            "name": "Charencon Geant",
            "char": "n",
            "color": libtcod.desaturated_blue,
            "brain": "BasicMonster",
            "hp": 20,
            "might": 3,
            "vitality": 5,
            "base_damage": (2, 5),
        },
        "gob_dog": {
            "name": "Chien goblin",
            "char": "c",
            "color": libtcod.desaturated_orange,
            "brain": "BasicMonster",
            "hp": 6,
            "might": 3,
            "vitality": 2,
            "base_damage": (2, 4),
        },
        "tertre_errant": {
            "name": "Tertre Errant",
            "char": "Y",
            "color": libtcod.desaturated_turquoise,
            "brain": "BasicMonster",
            "hp": 25,
            "might": 4,
            "vitality": 4,
            "base_damage": (1, 3),
        },
    }


def get_monster_stats(monster):
    try:
        return MonsterCompendium.monster_compendium[monster]
    except:
        return None


def get_base_monster_stats(base_monster):
    try:
        return BaseMonsterCompendium.base_monster_compendium[base_monster]
    except:
        return None
