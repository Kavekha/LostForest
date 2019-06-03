HEIGHT = 20
WIDTH = 10


class Test:
    def __init__(self, destructible=True):
        self.destructible = destructible

    def __repr__(self):
        if self.destructible:
            return '-'
        else:
            return '+'

class TestMap:
    def __init__(self):
        self.tiles = create_map()

    def __repr__(self):
        game_map = ''
        for x in self.tiles:
            game_map += str(x) + '\n'

        return game_map

    def _make_undestructible_barriers(self):
        # pour toutes les tuiles de x 0 et x Final.
        for y in range(0, HEIGHT):
            self.tiles[0][y].destructible = False
            self.tiles[WIDTH - 1][y].destructible = False

        for x in range(0, WIDTH):
            self.tiles[x][0].destructible = False
            self.tiles[x][HEIGHT - 1].destructible = False


def create_map():
    tiles = [[Test() for y in range(HEIGHT)] for x in range(WIDTH)]
    return tiles


game_map = TestMap()
print(game_map)
game_map._make_undestructible_barriers()
print(game_map)
