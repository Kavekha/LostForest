class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        # basics
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name

        # fov # TODO : Ne devrait pas être pour les entités pures, plutot les Vivants.
        self.fov_radius = 5
        self.light_walls = True

        self.blocks = blocks

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


# Permets de savoir s'il y a une entité bloquante à un emplacement. # TODO: Où placer cette fonctionnalité?
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
