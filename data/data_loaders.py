import shelve
import os


def load_game(file):
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError
    else:
        data_file = shelve.open(file, flag='r')
        try:
            game = data_file['game']
            data_file.close()
            return game
        except Exception:
            print('ERROR load')


def save_game(game):
    filename = 'savegame'
    data_file = shelve.open(filename)
    try:
        data_file['game'] = game
        data_file.close()
    except Exception:
        print('ERROR save')

