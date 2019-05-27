import libtcodpy as libtcod

'''
to put in entity.ai.
If an entity has it, then it is sentient.
'''


class Brain:
    def __init__(self):
        self.owner = None

    def take_turn(self, game_map, target, events):
        pass


class Brainless(Brain):
    # Sentient, but can't interact.
    pass

class BasicMonster(Brain):
    def take_turn(self, game_map, target, events):
        monster = self.owner
        if libtcod.map_is_in_fov(game_map.fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(game_map, target)
            elif target.fighter.hp > 0:
                monster.fighter.attack(target, events)
