from menus.menu import Menu
from menus.level_menu import LevelUpMenu
from data_loaders.localization import Texts


class CharacterMenu(Menu):
    def __init__(self, entity):
        super().__init__(entity)
        self.source = entity
        self.header = entity.name
        self.background_image = None  # libtcod.image_load('menu_background.png')
        self._options = []
        self.display_options = None
        self.forced_width = None
        self.update_options()

    def update_options(self):
        self.header = (
            ' {} '.format(self.source.name)
            + "  -  "
            + Texts.get_text('LEVEL_GAME_TERM') + ' {}'.format(self.source.level.current_level)
            + "\n"
            + """----------------------------------------


"""
            + Texts.get_text('MAX_HP_GAME_TERM')
            + ' : {} + {} \n'.format(self.source.fighter.base_max_hp,
                                      self.source.fighter.max_hp - self.source.fighter.base_max_hp)
            + Texts.get_text('MIGHT_GAME_TERM')
            + ' : {} + {} \n'.format(self.source.fighter.base_might,
                                      self.source.fighter.might - self.source.fighter.base_might)
            + Texts.get_text('DEXTERITY_GAME_TERM')
            + ' : {} + {} \n'.format(self.source.fighter.base_dexterity,
                                     self.source.fighter.dexterity - self.source.fighter.base_dexterity)
            + Texts.get_text('VITALITY_GAME_TERM')
            + ' : {} + {} \n'.format(self.source.fighter.base_vitality,
                                     self.source.fighter.vitality - self.source.fighter.base_vitality)
            + '\n \n'
            + Texts.get_text('PHYSICAL_POWER_GAME_TERM')
            + ' : {} '.format(self.source.fighter.physical_power)
            + '\n'
            + Texts.get_text('PHYSICAL_RESISTANCE_GAME_TERM')
            + ' : {} '.format(self.source.fighter.physical_resistance)
            + '\n \n'
            + Texts.get_text('WEAPON_DAMAGE_GAME_TERM')
            + ' : {} \n'.format(self.source.fighter.damage)
            + """


{} / {} """.format(self.source.level.current_xp,
                   self.source.level.experience_to_next_level)
            + Texts.get_text('UNTIL_NEXT_LEVEL_CHAR_SCREEN')
            + """

----------------------------------------

"""
        )

        if self.source.level.available_stat_points:
            self._options = ["level_up_screen"]
            self.display_options = [
                Texts.get_text('CHOOSE_STATS_INCREASE_CHAR_SCREEN') + ' ({})'.format(
                    self.source.level.available_stat_points
                )
            ]
        else:
            self._options = []

    def return_choice_result(self, string_choice):
        if string_choice == "level_up_screen":
            self.source.game.current_menu = LevelUpMenu(self.source)
