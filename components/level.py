from config.constants import ConstLevel, ConstTexts, ConstColors
from menus.character_menu import CharacterMenu


class Level:
    def __init__(self, current_level=1, current_xp=0):
        self.owner = None
        self.current_level = current_level
        self.current_xp = current_xp
        self.available_stat_points = 0

    @property
    def experience_to_next_level(self):
        return ConstLevel.LEVEL_UP_BASE + self.current_level * ConstLevel.LEVEL_UP_FACTOR

    def add_xp(self, xp, events):
        self.current_xp += xp
        print('gain xp : {}. Needed : {} / {}'.format(xp, self.current_xp, self.experience_to_next_level))

        self.check_level_up(events)

    def check_level_up(self, events):
        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1
            self.leveled_up(events)
            # on recheck si mega gain xp
            self.check_level_up(events)

    def leveled_up(self, events):
        self.available_stat_points += 1
        events.add_event({'message': ConstTexts.LEVEL_UP.format(self.current_level),
                          'color': ConstColors.POSITIVE_INFO_COLOR,
                          'level_up': self.owner})

    def show_character_screen(self):
        game = self.owner.game
        game.current_menu = self.create_character_menu()

    def create_character_menu(self):
        character_screen = CharacterMenu(self.owner)
        return character_screen
