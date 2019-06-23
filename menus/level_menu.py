from menus.menu import Menu
from data_loaders.localization import Texts
from config import game_config


class LevelUpMenu(Menu):
    def __init__(self, entity):
        super().__init__(entity)
        if entity.fighter and self.source.level.available_stat_points:
            self.update_options()

    def update_options(self):
        self.header = Texts.get_text('LEVEL_UP_MENU_HEADER').format(
            self.source.level.available_stat_points
        )
        self.display_options = [Texts.get_text('MIGHT_GAME_TERM'),
                                Texts.get_text('DEXTERITY_GAME_TERM'),
                                Texts.get_text('VITALITY_GAME_TERM')
                                ]
        self._options = ["Might", 'Dexterity', "Vitality"]

    def return_choice_result(self, string_choice):
        string_choice = string_choice.lower()
        if string_choice == "might":
            self.source.fighter.base_might += 1
        elif string_choice == "dexterity":
            self.source.fighter.base_dexterity += 1
        elif string_choice == "vitality":
            self.source.fighter.base_vitality += 1

        # on augmente aussi HP Max.
        hp_gain = 1 * game_config.HP_GAIN_AT_LEVEL__UP
        self.source.fighter.base_max_hp += hp_gain
        self.source.fighter.hp += hp_gain
        self.source.level.available_stat_points -= 1
        if self.source.level.available_stat_points > 0:
            self.update_options()
        else:
            self.source.level.show_character_screen()
