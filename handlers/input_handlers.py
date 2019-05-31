import libtcodpy as libtcod
from states.game_states import GameStates
from systems.commands import *


# Command version of inputhandler. v0.0.14
class InputHandler:
    def __init__(self, app, command_controller):
        self.app = app
        self.user_command_controller = command_controller

    def press(self, key):
        # key comes from libtcod.
        key = self.convert_libtcod_to_key(key)
        key = self.get_command_from_key(key)
        self.command_requested(key)

    def convert_libtcod_to_key(self, key):
        key_char = chr(key.c)

        if key.vk == libtcod.KEY_UP:
            return 'button_arrow_up'
        elif key.vk == libtcod.KEY_DOWN:
            return 'button_arrow_down'
        elif key.vk == libtcod.KEY_LEFT:
            return 'button_arrow_left'
        elif key.vk == libtcod.KEY_RIGHT:
            return 'button_arrow_right'

        if key_char == 'z':
            return 'button_z'
        elif key_char == 'g':
            return 'button_g'
        elif key_char == 'j':
            return 'button_j'

        return

    def get_command_from_key(self, key):
        if key == 'button_arrow_up':
            return 'move_up'
        elif key == 'button_arrow_down':
            return 'move_down'
        elif key == 'button_arrow_left':
            return 'move_left'
        elif key == 'button_arrow_right':
            return 'move_right'
        elif key == 'button_z':
            return 'wait'
        elif key == 'button_g':
            return 'pick_up'
        elif key == 'button_j':
            return 'take_stairs'

        return

    def command_requested(self, cmd):
        if not cmd:
            return
        else:
            cmd = cmd.strip().lower()
            if cmd == 'move_up':
                self.user_command_controller.execute(MoveUpCommand(self.app.game.player))
            elif cmd == 'move_down':
                self.user_command_controller.execute(MoveDownCommand(self.app.game.player))
            elif cmd == 'move_left':
                self.user_command_controller.execute(MoveLeftCommand(self.app.game.player))
            elif cmd == 'move_right':
                self.user_command_controller.execute(MoveRightCommand(self.app.game.player))
            elif cmd == 'wait':
                self.user_command_controller.execute(WaitCommand(self.app.game.player))
            elif cmd == 'pick_up':
                self.user_command_controller.execute(PickUpCommand(self.app.game.player))
            elif cmd == 'take_stairs':
                self.user_command_controller.execute(TakeStairsCommand(self.app.game.player))


# TODO : Repetitions de l'effet Fullscreen et Exit.
def handle_keys(key, game_state):
    action = {'app': {}, 'game': {}}

    if game_state == GameStates.PLAYERS_TURN:
        action = handle_player_turn_keys(key)

    elif game_state == GameStates.PLAYER_DEAD:
        action = handle_player_dead_keys(key)

    elif game_state == GameStates.SHOW_INVENTORY:
        action = handle_player_options_keys(key)

    return action


def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        # print('handle main menu: new_game')
        return {'new_game': True}
    elif key_char == 'b':
        # print('handle main menu: load_game')
        return {'load_save_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        # print('handle main menu: app_exit')
        return {'app_exit': True}

    return {}


# Originaly meant for inventory.
# CHECK : To make more generic for other situation where keys = options from a list
def handle_player_options_keys(key):
    action = {'app': {}, 'game': {}}

    # converting the key pressed to an index. 'a' will be 0, 'b' will be 1, and so on.
    index = key.c - ord('a')

    if index >= 0:
        action['game'] = {'game_option_choice': index}

    # others
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        action['app'] = {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        action['game'] = {'exit': True}

    # No key was pressed
    return action


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    action = {'app': {}, 'game': {}}

    if key_char == 'i':
        action['game'] = {'show_inventory': True}

    # others
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        action['app'] = {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        action['game'] = {'exit': True}
        action['app'] = {'exit': True}

    # No key was pressed
    return action


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    action = {'app': {}, 'game': {}}
    # Movement keys
    if key_char == 'i':
        action['game'] = {'show_inventory': True}

    # others
    '''
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        action['app'] = {'fullscreen': True}
    '''
    if key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        action['game'] = {'exit': True}
        action['app'] = {'exit': True}

    # No key was pressed
    return action

