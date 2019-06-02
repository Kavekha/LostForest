from render_engine import RenderOrder
from entities import Entity, EntityType, is_entity_type
import libtcodpy as libtcod
from config.constants import ConstTexts, ConstColors


class TargetType:
    NONE = 0
    SELF = 1
    FIGHTING_ENTITY = 2
    ITEM_ENTITY = 3


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
        elif self.target_type == TargetType.SELF:
            # on lance directement l effet sur soit, sans selection possible.
            self.check_target_against_wanted_type({'entity_fighter': self.player})
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

    def get_info_from_tile(self):
        print('target: get info')
        results = {}
        x, y = self.x, self.y
        entities = self.game_map.get_entities()
        print('my position is : ', x, y)
        for entity in entities:
            if entity != self:
                if entity.x == x and entity.y == y:
                    if is_entity_type(entity, EntityType.FIGHTER):
                        print('it s a fighter')
                        results['entity_fighter'] = entity
                    elif is_entity_type(entity, EntityType.ITEM):
                        print('it s an item')
                        results['entity_item'] = entity
        print('results is ', results)
        return results

    def validate_target(self):
        results = self.get_info_from_tile()
        self.check_target_against_wanted_type(results)

    def check_target_against_wanted_type(self, results_dict):
        if self.target_type in [TargetType.FIGHTING_ENTITY, TargetType.SELF]:
            entity_fighter = results_dict.get('entity_fighter')
            if entity_fighter:
                self.play_function_on_target(entity_fighter)
            else:
                self.game.events.add_event({'message': 'You must select a fighting entity',
                                            'color': ConstColors.TARGET_ERROR_COLOR})

        elif self.target_type == TargetType.ITEM_ENTITY:
            entity_item = results_dict.get('entity_item')
            if entity_item:
                self.play_function_on_target(entity_item)
            else:
                self.game.events.add_event({'message': 'You must select an item entity',
                                            'color': ConstColors.TARGET_ERROR_COLOR})

        else:
            self.game.events.add_event({'message': 'Your target is of the wrong type',
                                        'color': ConstColors.TARGET_ERROR_COLOR})

    def play_function_on_target(self, target):
        # TODO: item only, make it more generic
        item_use_results = self.function_on_validate(self.player, self.target_source, target, self.game.events)
        print('play function : target source is : ', self.target_source)
        self.player.inventory.resolve_use_results(item_use_results, self.target_source.owner, self.game.events)

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
