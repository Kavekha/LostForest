class Tile:
    def __init__(self, blocked, block_sight=None, destructible=False):
        self.destructible = destructible
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = {}

    def has_been_explored(self, x, y):
        return self.explored.get((x, y), False)

    def discovered(self, x, y):
        self.explored[(x, y)] = True




class Terrain:
    GROUND = Tile(False, destructible=False)
    NATURAL_WALL = Tile(True, destructible=True)
    INDESTRUCTIBLE_NATURAL_WALL = Tile(True, destructible=False)



