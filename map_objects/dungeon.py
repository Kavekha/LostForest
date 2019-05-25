from config.dungeon_config import get_dungeon_config
from map_objects.map import GameMap
from config.constants import ConstColors, ConstTexts


class Dungeon:
    def __init__(self, game, name='dungeon'):
        self.game = game
        self.name = name
        self.current_floor = 1
        self.current_map = None

        config = get_dungeon_config()
        self.max_floor = config['max_floor']

    def generate_floor(self):
        self.current_map = GameMap(self)
        self.current_map.add_player(self.game.player)
        self.current_map.generate_map(self.game.player)

    def next_floor(self):
        new_floor = self.current_floor + 1
        if new_floor <= self.max_floor:
            self.current_floor += 1
            self.generate_floor()
            self.game.recompute_fov()
            # empecher artefacts de la carte precedente. Fix merdique. Dans Engine, render et Game aussi.
            self.game.reset_game_windows = True

            self.game.player.fighter.heal(self.game.player.fighter.max_hp // 2)
            self.game.events.add_event({'message': ConstTexts.REST_AFTER_STAIRS,
                                        'color': ConstColors.REST_AFTER_STAIRS_COLOR})
        else:
            self.game.events.add_event({'message': ConstTexts.VICTORY_LAST_FLOOR_BASIC,
                                        'color': ConstColors.POSITIVE_INFO_COLOR})





