from random import randint
import libtcodpy as libtcod
from entities import Entity

class Spawner:
    def __init__(self, map):
        self.map_owner = map

    def spawn_entities(self):
        for room in self.map_owner.rooms:
            nb_monsters = randint(0, self.map_owner.max_monsters_room)

            for mob in range(nb_monsters):
                x = randint(room.x1 + 1, room.x2 - 1)
                y = randint(room.y1 + 1, room.y2 - 1)

                # ici on check si il existe deja des entités à cet endroit.
                if not any([entity for entity in self.map_owner.entities if entity.x == x and entity.y == y]):
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Ougloth', blocks=True)  # TODO : Table de spawn de mob
                    self.map_owner.add_entity(monster)
