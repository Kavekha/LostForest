from menus.menu import Menu
from menus.level_menu import LevelUpMenu


class CharacterMenu(Menu):
    def __init__(self, entity):
        super().__init__(entity)
        self.header = entity.name
        self.background_image = None  # libtcod.image_load('menu_background.png')
        self._options = []
        self.display_options = None
        self.forced_width = 48
        self.update_options()

    def update_options(self):
        self.header = self.source.name + '  -  ' + 'Level {}'.format(
            self.source.level.current_level) + '\n' + '''----------------------------------------


Max HP : {0} + {1}
Might : {2} + {3}
Vitality : {4} + {5}

Damages : {8}


{6} / {7} until next level

----------------------------------------

'''.format(self.source.fighter.base_max_hp, (self.source.fighter.max_hp - self.source.fighter.base_max_hp),
           self.source.fighter.base_might, (self.source.fighter.might - self.source.fighter.base_might),
           self.source.fighter.base_vitality, (self.source.fighter.vitality - self.source.fighter.base_vitality),
           self.source.level.current_xp, self.source.level.experience_to_next_level,
           self.source.fighter.damage)

        if self.source.level.available_stat_points:
            self._options = ['level_up_screen']
            self.display_options = ['Choose stat to increase ({})'.format(self.source.level.available_stat_points)]
        else:
            self._options = []

    def return_choice_result(self, string_choice):
        if string_choice == 'level_up_screen':
            self.source.game.current_menu = LevelUpMenu(self.source)
