from systems.target_selection import Target


class CommandController:
    def execute(self, command):
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
        if self._obj.level:
            self._obj.level.show_character_screen()


# TARGET
class ValidateTarget(Command):
    def execute(self):
        if isinstance(self._obj, Target):
            self._obj.validate_target()


# INVENTORY
class ShowInventory(Command):
    def execute(self):
        if self._obj.inventory:
            self._obj.inventory.show_inventory("use")


class DropMenu(Command):
    def execute(self):
        if self._obj.inventory:
            self._obj.inventory.show_inventory("drop")


# CHARACTER
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
        if self._obj.inventory:
            self._obj.inventory.pick_up()


class TakeLandmarkCommand(Command):
    def execute(self):
        self._obj.take_landmark()
