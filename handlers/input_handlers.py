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

    #if action != {'app': {}, 'game': {}}:
    #    print('action is : ', action)

    return action


# Originaly meant for inventory.
# CHECK : To make more generic for other situation where keys = options from a list
def handle_player_options_keys(key):
    action = {'app': {}, 'game': {}}

    # converting the key pressed to an index. 'a' will be 0, 'b' will be 1, and so on.
    index = key.c - ord('a')

    if index >= 0:
        action['game'] = {'game_option_choice': index}
        if action['game'] == 0:
            print('index : 0')

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

