import shelve
import os

from config import app_config
from utils.fov_functions import initialize_fov
from states.app_states import AppStates


def load_game(file):
    filename = app_config.SAVE_DIRECTORY + file
    if not os.path.isfile(filename + '.dat'):
        print()
        raise FileNotFoundError
    else:
        data_file = shelve.open(filename, flag="c")
        try:
            game = data_file["game"]
            data_file.close()
            return game
        except AttributeError:
            # 'nonetype object has no attribute dungeon'    TODO
            print("ERROR load")
        except KeyError:
            # value = self.cache[key]  # KeyError: 'game'
            print('ERROR: Ne trouve pas game?')


def save_game(game):
    with shelve.open(app_config.SAVE_DIRECTORY + "savegame", flag='n') as data_file:
        try:
            data_file['game'] = game
        except Exception:
            print('ERROR SAVE')


def refresh_at_load(source):

    # This is needed so the map & chars are fully rendered.
    source.game.dungeon.current_map.fov_map = initialize_fov(
        source.game.dungeon.current_map
    )
    source.game.full_recompute_fov()
    source.game.app = source  # On associe Game à App.
    source.app_states = AppStates.GAME
    source.reset_game_windows = True
    source.render_engine.reset_render_windows()
    source.current_menu = None
