from config.dungeon_config import get_dungeon_config
from map_objects.map import GameMap
from config.constants import ConstColors, ConstTexts


class Dungeon:
    def __init__(self, game, name='dungeon'):
        self.game = game
        self.name = name
        self.current_floor = 1
        self.current_map = None

        config = get_dungeon_config(self.name)
        self.max_floor = config['max_floor']
        self.floors = config['floors']

    def initialize(self):
        self.generate_floor(self.get_floor_to_create())

    def get_floor_to_create(self):
        current_floor = self.current_floor
        map_to_create = None
        while not map_to_create:
            try:
                map_to_create = self.floors[str(current_floor)]
            except:
                current_floor -= 1
                if current_floor == 0:
                    map_to_create = 'standard_map'
        return map_to_create

    def generate_floor(self, map_to_create):
        self.current_map = GameMap(self, map_to_create)
        self.current_map.add_player(self.game.player)
        self.current_map.generate_map(self.game.player)

    def next_floor(self):
        new_floor = self.current_floor + 1
        if new_floor <= self.max_floor:
            self.current_floor += 1
            self.generate_floor(self.get_floor_to_create())
            self.game.recompute_fov()
            # empecher artefacts de la carte precedente. Fix merdique. Dans Engine, render et Game aussi.
            self.game.reset_game_windows = True

            self.game.player.fighter.heal(self.game.player.fighter.max_hp // 2)
            self.game.events.add_event({'message': ConstTexts.REST_AFTER_STAIRS,
                                        'color': ConstColors.REST_AFTER_STAIRS_COLOR})
        else:
            self.game.events.add_event({'message': ConstTexts.VICTORY_LAST_FLOOR_BASIC,
                                        'color': ConstColors.POSITIVE_INFO_COLOR})





