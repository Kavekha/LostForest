class CommandController:
    def __init__(self):
        self.history = []

    def execute(self, command):
        self.history.append(command)
        command.execute()


class Command(object):
    def __init__(self, obj):
        self._obj = obj

    def execute(self):
        raise NotImplementedError


# APPLICATION
class FullScreenCommand(Command):
    def execute(self):
        self._obj.full_screen()


class ExitWindow(Command):
    def execute(self):
        self._obj.exit_window()


# IN GAME : ENTITY

# LEVEL
class ShowCharacterScreen(Command):
    def execute(self):
        self._obj.show_character_screen()


# INVENTORY
class ShowInventory(Command):
    def execute(self):
        self._obj.show_inventory()


class MoveUpCommand(Command):
    def execute(self):
        self._obj.try_to_move(0, -1)


class MoveDownCommand(Command):
    def execute(self):
        self._obj.try_to_move(0, 1)


class MoveLeftCommand(Command):
    def execute(self):
        self._obj.try_to_move(-1, 0)


class MoveRightCommand(Command):
    def execute(self):
        self._obj.try_to_move(1, 0)


class WaitCommand(Command):
    def execute(self):
        self._obj.wait()


class PickUpCommand(Command):
    def execute(self):
        self._obj.pick_up()


class TakeStairsCommand(Command):
    def execute(self):
        self._obj.take_stairs()
