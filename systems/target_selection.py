from render_engine import RenderOrder
from entities import Entity
import libtcodpy as libtcod
from config.constants import ConstTexts, ConstColors


class TargetType:
    NONE = 0
    SELF = 1
    OTHER = 2


class Target(Entity):
    def __init__(self, player, game, target_source, target_type):
        super().__init__(game, player.x, player.y, '+', libtcod.white, 'Target')
        self.target_source = target_source
        self.function_on_validate = target_source.use_function
        self.player = player
        self.game_map = game.dungeon.current_map
        self.render_order = RenderOrder.TARGET
        self.target_type = target_type

        if self.target_type == TargetType.NONE:
            self.game.events.add_event({'message': ConstTexts.TARGET_TYPE_INVALID,
                                        'color': ConstColors.TARGET_MESS_COLOR})
            self.quit_target_mode()
        else:
            # Je m'ajoute pour être visible.
            self.game_map.add_entity(self)
            self.warning()

    def quit_target_mode(self):
        self.game.events.add_event({'quit_target_mode': True})

    def warning(self):
        self.game.events.add_event({'message': ConstTexts.TARGET_MODE_ON, 'color': ConstColors.TARGET_MESS_COLOR})
        self.game.events.add_event({'message': ConstTexts.TARGET_CONTROLS_EXPLAIN,
                                    'color': ConstColors.TARGET_MESS_COLOR})

    def validate_target(self):
        self.game.events.add_event({'message': 'You validate something', 'color': ConstColors.TARGET_MESS_COLOR})
        self.game.events.add_event({'function_to_play': self.function_on_validate(self.player,
                                                                                  self.target_source.power,
                                                                                  self.player)})
        self.quit_target_mode()

    def wait(self):
        self.warning()
        self.player.wait()
        # super().wait()

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def try_to_move(self, dx, dy):
        destination_x = self.x + dx
        destination_y = self.y + dy
        if libtcod.map_is_in_fov(self.game_map.fov_map, destination_x, destination_y):
            self.move(dx, dy)

    def interact_with_entity(self, entity):
        raise NotImplementedError

    def move_towards(self, target_x, target_y):
        raise NotImplementedError

    def distance_to(self, other):
        raise NotImplementedError

    def move_astar(self, game_map, target):
        raise NotImplementedError
