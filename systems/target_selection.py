from render_engine import RenderOrder
from entities import Entity, EntityType, is_entity_type
import tcod as libtcod
from config.constants import ConstTexts, ConstColors


class TargetType:
    NONE = 0
    SELF = 1
    FIGHTING_ENTITY = 2
    ITEM_ENTITY = 3
    OTHER_ENTITY = 4
    TILE = 5


class Target(Entity):
    def __init__(self, player, game, target_source, target_type):
        super().__init__(game, player.x, player.y, "+", libtcod.white, "Target")
        self.target_source = target_source
        self.function_on_validate = target_source.use_function
        self.player = player
        self.game_map = game.dungeon.current_map
        self.render_order = RenderOrder.TARGET
        self.target_type = target_type

        self.game_map.add_entity(self)

        if self.target_type == TargetType.NONE:
            self.game.events.add_event(
                {
                    "message": ConstTexts.TARGET_TYPE_INVALID,
                    "color": ConstColors.TARGET_MESS_COLOR,
                }
            )
            self.quit_target_mode()
        elif self.target_type == TargetType.SELF:
            # on lance directement l effet sur soit, sans selection possible.
            self.play_function_on_target(
                {
                    "requested": self.player,
                    "not_requested": [],
                    "tile": self.get_map_tile(self.x, self.y),
                }
            )
        else:
            self.warning()

    def quit_target_mode(self):
        self.game.events.add_event({"quit_target_mode": True})

    def warning(self):
        self.game.events.add_event(
            {
                "message": ConstTexts.TARGET_MODE_ON,
                "color": ConstColors.TARGET_MESS_COLOR,
            }
        )
        self.game.events.add_event(
            {
                "message": ConstTexts.TARGET_CONTROLS_EXPLAIN,
                "color": ConstColors.TARGET_MESS_COLOR,
            }
        )

    def get_map_entities(self):
        return self.game_map.get_entities()

    def get_map_tile(self, x, y):
        return self.game_map.tiles[x][y]

    def validate_target(self):
        results, valid = self.get_info_from_tile()
        # on envoie les resultats, meme si not valid, pour messages sympas & rigolos potentiels.
        if results:
            self.play_function_on_target(results)
        if not valid:
            self.game.events.add_event(
                {
                    "message": "Your target is of the wrong type",
                    "color": ConstColors.TARGET_ERROR_COLOR,
                }
            )
        self.quit_target_mode()

    def play_function_on_target(self, dict_target):
        # TODO: item only, make it more generic
        item_use_results = self.function_on_validate(
            self.player, self.target_source, dict_target, self.game.events
        )
        print("play function : target source is : ", self.target_source)
        self.player.inventory.resolve_use_results(
            item_use_results, self.target_source.owner, self.game.events
        )

        self.quit_target_mode()

    def is_wanted_type(self, targeted_object_type):
        if targeted_object_type == self.target_type:
            return True
        else:
            return False

    def get_info_from_tile(self):
        results = {"requested": None, "not_requested": [], "tile": None}

        x, y = self.x, self.y
        entities = self.get_map_entities()
        for entity in entities:
            if entity.x == x and entity.y == y:
                if entity != self:
                    if is_entity_type(entity, EntityType.FIGHTER):
                        if self.is_wanted_type(TargetType.FIGHTING_ENTITY):
                            results["requested"] = entity
                        else:
                            results["not_requested"].append(entity)
                    elif is_entity_type(entity, EntityType.ITEM):
                        if self.is_wanted_type(TargetType.ITEM_ENTITY):
                            results["requested"] = entity
                        else:
                            results["not_requested"].append(entity)
                    else:
                        if self.is_wanted_type(TargetType.OTHER_ENTITY):
                            results["requested"] = entity
                        else:
                            results["not_requested"].append(entity)
                else:
                    if self.is_wanted_type(TargetType.SELF):
                        results["requested"] = entity
                    else:
                        results["not_requested"].append(entity)
        results["tile"] = self.get_map_tile(x, y)

        requested = results.get("requested")
        print("target result is : ", results)

        return results, requested

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
