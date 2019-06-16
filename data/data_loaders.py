import shelve
import os


def load_game(file):
    if not os.path.isfile("savegame.dat"):
        raise FileNotFoundError
    else:
        data_file = shelve.open(file, flag="c")
        try:
            game = data_file["game"]
            data_file.close()
            return game
        except Exception:
            print("ERROR load")


def save_game(game):
    filename = "savegame"
    with shelve.open(filename, flag='n') as data_file:
        try:
            data_file['game'] = game
        except Exception:
            print('ERROR SAVE')
