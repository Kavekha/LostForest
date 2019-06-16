import tcod as libtcod
from states.app_states import AppStates
from systems.commands import *


# Command version of inputhandler. v0.0.14
class InputHandler:
    def __init__(self, app, command_controller):
        self.app = app
        self.user_command_controller = command_controller

    def get_current_menu(self):
        current_menu = None
        if self.app.game and self.app.game.current_menu:
            current_menu = self.app.game.current_menu
        elif self.app.current_menu:
            current_menu = self.app.current_menu

        return current_menu

    def press(self, key):
        current_menu = self.get_current_menu()
        # key comes from libtcod.
        converted_key = self.convert_libtcod_to_key(key)
        command_key = self.get_command_from_key(converted_key)

        if current_menu:
            index = key.c - ord("a")
            if index >= 0:
                current_menu.receive_option_choice(index)

        self.command_requested(command_key)

    def convert_libtcod_to_key(self, key):
        key_char = chr(key.c)

        if key.vk == libtcod.KEY_UP:
            return "button_arrow_up"
        elif key.vk == libtcod.KEY_DOWN:
            return "button_arrow_down"
        elif key.vk == libtcod.KEY_LEFT:
            return "button_arrow_left"
        elif key.vk == libtcod.KEY_RIGHT:
            return "button_arrow_right"

        if key_char == "z":
            return "button_z"
        elif key_char == "g":
            return "button_g"
        elif key_char == "j":
            return "button_j"
        elif key_char == "i":
            return "button_i"
        elif key_char == "c":
            return "button_c"
        elif key_char == "d":
            return "button_d"

        if key.vk == libtcod.KEY_ESCAPE:
            return "button_escape"

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            return "button_alt_enter"

        if key.vk == libtcod.KEY_SPACE:
            return "button_space"

        return

    def get_command_from_key(self, key):
        if key == "button_arrow_up":
            return "move_up"
        elif key == "button_arrow_down":
            return "move_down"
        elif key == "button_arrow_left":
            return "move_left"
        elif key == "button_arrow_right":
            return "move_right"
        elif key == "button_z":
            return "wait"
        elif key == "button_g":
            return "pick_up"
        elif key == "button_j":
            return "take_landmark"
        elif key == "button_i":
            return "show_inventory"
        elif key == "button_c":
            return "character_screen"
        elif key == "button_d":
            return "drop_menu"
        elif key == "button_space":
            return "validate_target"

        if key == "button_alt_enter":
            return "full_screen"
        elif key == "button_escape":
            return "exit_window"

        return

    def command_requested(self, cmd):
        if not cmd:
            return
        else:
            cmd = cmd.strip().lower()
            if self.app.app_states == AppStates.GAME and not self.app.game.current_menu:
                if not self.app.game.target_mode:
                    obj = self.app.game.player
                else:
                    obj = self.app.game.target

                # On char or Target
                if cmd == "move_up":
                    self.user_command_controller.execute(MoveUpCommand(obj))
                # On char or Target
                elif cmd == "move_down":
                    self.user_command_controller.execute(MoveDownCommand(obj))
                # On char or Target
                elif cmd == "move_left":
                    self.user_command_controller.execute(MoveLeftCommand(obj))
                # On char or Target
                elif cmd == "move_right":
                    self.user_command_controller.execute(MoveRightCommand(obj))
                # On char or Target
                elif cmd == "wait":
                    self.user_command_controller.execute(WaitCommand(obj))
                elif cmd == "pick_up":
                    self.user_command_controller.execute(PickUpCommand(obj))
                elif cmd == "take_landmark":
                    self.user_command_controller.execute(TakeLandmarkCommand(obj))
                elif cmd == "show_inventory":
                    self.user_command_controller.execute(ShowInventory(obj))
                elif cmd == "character_screen":
                    self.user_command_controller.execute(ShowCharacterScreen(obj))
                elif cmd == "drop_menu":
                    self.user_command_controller.execute(DropMenu(obj))
                elif cmd == "validate_target":
                    self.user_command_controller.execute(ValidateTarget(obj))

            if cmd == "exit_window":
                self.user_command_controller.execute(ExitWindow(self.app))
