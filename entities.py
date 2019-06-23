import tcod as libtcod

import math

from render_engine import RenderOrder
from data_loaders.localization import Texts
from config import color_config
from components.item import Item


class EntityType:
    ENTITY = 0
    FIGHTER = 1
    ITEM = 2


def is_entity_type(entity, entity_type):
    if entity_type == EntityType.ENTITY:
        if isinstance(entity, Entity):
            return True
    if entity_type == EntityType.FIGHTER:
        if is_entity_type(entity, EntityType.ENTITY) and entity.fighter:
            return True
    if entity_type == EntityType.ITEM:
        if is_entity_type(entity, EntityType.ENTITY) and entity.item:
            return True
    return False


# TODO: Pas ouf de remonter comme ca aussi haut pour recuperer le game.
# TODO: Pertinence du Game dans Entity
class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(
            self,
            game,
            x,
            y,
            char,
            color,
            name,
            blocks=False,
            fighter=None,
            ai=None,
            inventory=None,
            item=None,
            landmark=None,
            level=None,
            equipment=None,
            equippable=None,
            render_order=RenderOrder.CORPSE):
        # basics
        self.game = game
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.render_order = render_order
        self.kill_function = None
        self.round = game.round

        # components
        component_list = [
            fighter,
            ai,
            inventory,
            item,
            landmark,
            level,
            equipment,
            equippable,
        ]
        self.fighter = fighter
        self.ai = ai
        self.inventory = inventory
        self.item = item
        self.landmark = landmark
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.add_component(component_list)

        # An equipable entity must be an item
        if self.equippable and not self.item:
            item = Item()
            self.item = item
            self.item.owner = self

        # fov # TODO : Ne devrait pas être pour les entités pures, plutot les Vivants.
        self.fov_radius = 5
        self.light_walls = True

        self.blocks = blocks

    def add_component(self, component_list):
        for component in component_list:
            if component:
                component.owner = self
            else:
                continue

    def end_turn(self):
        self.round += 1

    def wait(self):
        self.end_turn()

    def pick_up(self):
        if self.inventory:
            result = self.inventory.pick_up()  # True if success.
            if result:
                self.end_turn()

    def take_landmark(self):
        entities = self.game.dungeon.current_map.get_entities()

        for entity in entities:
            if entity.landmark and entity.x == self.x and entity.y == self.y:
                self.game.dungeon.next_floor()
                self.game.full_recompute_fov()
                self.end_turn()
                break
        else:
            self.game.events.add_event(
                {
                    "message": Texts.get_text('NO_LANDMARK_THERE'),
                    "color": color_config.IMPORTANT_INFO_COLOR,
                }
            )

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
        self.end_turn()

    def try_to_move(self, dx, dy):
        # TODO: Si mort, peut pas bouger. Fait sens, mais vie dans Fighter et Move dans Entity.
        if self.fighter:
            if self.fighter.hp <= 0:
                return
        destination_x = self.x + dx
        destination_y = self.y + dy
        # s il n y a pas de tuile bloquante...
        if not self.game.dungeon.current_map.is_blocked(destination_x, destination_y):
            # y a t il des entités bloquantes?
            blocking_entity_at_destination = get_blocking_entities_at_location(
                self.game.dungeon.current_map.get_entities(), destination_x, destination_y
            )
            if blocking_entity_at_destination:
                self.interact_with_entity(blocking_entity_at_destination)
            else:
                self.move(dx, dy)

    def interact_with_entity(self, entity):
        if entity.fighter and self.fighter:
            # Nous sommes des guerriers, on se tape.
            self.fighter.attack(entity, self.game.events)
        self.end_turn()

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.try_to_move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_astar(self, game_map, target):
        width, height = game_map.get_map_sizes()
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(width, height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(height):
            for x1 in range(width):
                libtcod.map_set_properties(
                    fov,
                    x1,
                    y1,
                    not game_map.tiles[x1][y1].block_sight,
                    not game_map.tiles[x1][y1].blocked,
                )

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in game_map.get_entities():
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths
        # (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map
        # if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
                self.end_turn()
        else:
            # Keep the old move function as a backup so that if there are no paths
            # (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y)

            # Delete the path to free memory
        libtcod.path_delete(my_path)


# Permets de savoir s'il y a une entité bloquante à un emplacement.
# todo: on garde ici?
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
