class Tile:
    def __init__(self, name, blocked, block_sight=None, destructible=False, explored=False):
        self.name = name
        self.destructible = destructible
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = explored

        self._immutable = True

    def __setattr__(self, name, value):
        if getattr(self, '_immutable', False):
            raise RuntimeError('This object is immutable')
        else:
            super().__setattr__(name, value)
