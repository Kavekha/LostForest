from menus.menu import Menu
from systems.localization import Texts


class LevelUpMenu(Menu):
    def __init__(self, entity):
        super().__init__(entity)
        if entity.fighter and self.source.level.available_stat_points:
            self.update_options()

    def update_options(self):
        self.header = Texts.get_text('LEVEL_UP_MENU_HEADER').format(
            self.source.level.available_stat_points
        )
        self.display_options = []
        self._options = ["Might", "Vitality", "HP"]

    def return_choice_result(self, string_choice):
        string_choice = string_choice.lower()
        if string_choice == "might":
            self.source.fighter.base_might += 1
        elif string_choice == "vitality":
            self.source.fighter.base_vitality += 1
        elif string_choice == "hp":
            self.source.fighter.base_max_hp += 5
            self.source.fighter.hp += 5

        self.source.level.available_stat_points -= 1
        if self.source.level.available_stat_points > 0:
            self.update_options()
        else:
            self.source.level.show_character_screen()
