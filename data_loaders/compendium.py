import tcod as libtcod      # Needed for now a cause de la recuperation des couleurs dans le CSV...

import csv

from config import app_config


"""

On recoit un csv sous forme de

defname;name;char;color;brain;hp;might;dexterity;vitality;base_damage;armor

at the end we want this:

"ougloth": {
            "name": "Ougloth",
            "char": "o",
            "color": libtcod.dark_red,
            "brain": "BasicMonster",
            "hp": 10,
            "might": 4,
            "vitality": 3,
            "base_damage": (0, 2),
        }

"""


class Compendium:
    monster_base_compendium = {}
    monster_full_compendium = {}

    def __init__(self):
        Compendium.monster_base_compendium = Compendium.create_compendium_from_csv(
            app_config.DATA_DIRECTORY + 'monsters_base.csv'
        )
        Compendium.monster_full_compendium = Compendium.create_compendium_from_csv(
            app_config.DATA_DIRECTORY + 'monster_full.csv'
        )

    @staticmethod
    def create_compendium_from_csv(path):

        with open(path, 'r', encoding='utf-8') as csv_file:
            compendium_data = csv.reader(csv_file, delimiter=';')
            header = next(compendium_data)

            compendium = {}

            for row in compendium_data:
                if row:
                    defname = ''
                    compendium_stats = {}
                    for carac, value in zip(header, row):
                        if carac:
                            if carac == 'defname':
                                defname = value.lower()
                            elif carac == 'color' and value:
                                compendium_stats.update({carac: eval(value)})
                            else:
                                if not value:
                                    continue
                                compendium_stats.update({carac: value})
                                compendium.update({defname: compendium_stats})

        return compendium

    @staticmethod
    def get_monster(defname):
        return Compendium.monster_full_compendium.get(defname.lower(), None)

    @staticmethod
    def get_base_monster(defname):
        return Compendium.monster_base_compendium.get(defname.lower(), None)


Compendium()
print(f'Monster base compendium : {Compendium.monster_base_compendium}')
print(f'Monster full compendium : {Compendium.monster_full_compendium}')