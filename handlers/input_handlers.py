import libtcodpy as libtcod
from states.game_states import GameStates


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

    if key.vk == libtcod.KEY_UP:
        action['game'] = {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        action['game'] = {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        action['game'] = {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        action['game'] = {'move': (1, 0)}

    if key_char == 'g':
        action['game'] = {'pickup': True}
    elif key_char == 'i':
        print('handler: inventory')
        action['game'] = {'show_inventory': True}
    #elif key.vk == libtcod.KEY_ENTER:
    elif key_char == 'j':
        action['game'] = {'take_stairs': True}
    elif key_char == 'z':
        action['game'] = {'wait': True}

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

