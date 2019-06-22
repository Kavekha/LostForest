from config import game_config, color_config
from systems.localization import Texts
from menus.character_menu import CharacterMenu


class Level:
    def __init__(self, current_level=1, current_xp=0):
        self.owner = None
        self.current_level = current_level
        self.current_xp = current_xp
        self.available_stat_points = 0

    @property
    def experience_to_next_level(self):
        return (
            game_config.LEVEL_UP_BASE + self.current_level * game_config.LEVEL_UP_FACTOR
        )

    def add_xp(self, xp, events):
        self.current_xp += xp
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
        events.add_event(
            {
                "message": Texts.get_text('LEVEL_UP').format(self.current_level),
                "color": color_config.POSITIVE_INFO_COLOR,
                "level_up": self.owner,
            }
        )

    def show_character_screen(self):
        game = self.owner.game
        game.current_menu = self.create_character_menu()

    def create_character_menu(self):
        character_screen = CharacterMenu(self.owner)
        return character_screen
