from bearlibterminal import terminal as blt

import sys

from states.app_states import AppStates
from systems.commands import *


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
        converted_key = self.convert_blt_to_key(key)
        command_key = self.get_command_from_key(converted_key)

        if current_menu:
            index = blt.state(blt.TK_CHAR) - ord('a')
            if index >= 0:
                current_menu.receive_option_choice(index)

        self.command_requested(command_key)

    def convert_blt_to_key(self, key):
        if key == blt.TK_UP:
            return "button_arrow_up"
        elif key == blt.TK_DOWN:
            return "button_arrow_down"
        elif key == blt.TK_LEFT:
            return "button_arrow_left"
        elif key == blt.TK_RIGHT:
            return "button_arrow_right"

        if key == blt.TK_Z:
            return "button_z"
        elif key == blt.TK_G:
            return "button_g"
        elif key == blt.TK_J:
            return "button_j"
        elif key == blt.TK_I:
            return "button_i"
        elif key == blt.TK_C:
            return "button_c"
        elif key == blt.TK_D:
            return "button_d"

        if key == blt.TK_ESCAPE:
            return "button_escape"

        if key == blt.TK_ENTER and blt.state(blt.TK_ALT):
            return "button_alt_enter"

        if key == blt.TK_SPACE:
            return "button_space"

        if key == blt.TK_CLOSE:
            sys.exit()

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
