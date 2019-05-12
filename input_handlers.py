import libtcodpy as libtcod


def handle_keys(key):
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

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        action['app'] = {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        action['game'] = {'exit': True}

    # No key was pressed
    return action

