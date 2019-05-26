import libtcodpy as libtcod
from config.config import get_app_config
from handlers.input_handlers import handle_keys, handle_main_menu
from render_engine import Render
from game import Game
from states.app_states import AppStates
from data.data_loaders import load_game
from utils.fov_functions import initialize_fov


class App:
    def __init__(self):
        # app config
        config = get_app_config()

        # render engine
        screen_width = config['screen_width']
        screen_height = config['screen_height']
        bar_width = config['bar_width']
        panel_height = config['panel_height']
        main_menu_background_image = libtcod.image_load('menu_background.png')
        self.render_engine = Render(main_menu_background_image, screen_width, screen_height, bar_width, panel_height)

        self.app_states = AppStates.MAIN_MENU
        self.box_message = None

        self.game = None

    def run(self):
        # initialize controls.
        key = libtcod.Key()
        mouse = libtcod.Mouse()

        # main loop
        while not libtcod.console_is_window_closed():
            # check key / mouse event
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

            # TODO: Faut bien savoir ce que l'on rends, d'où les state Apps.
            # TODO : Action handler : chiant de devoir le faire pour chaque State, en tout cas comme ca.
            if self.app_states in (AppStates.MAIN_MENU, AppStates.BOX):
                self.render_engine.render_main_menu(self)

                action = handle_main_menu(key)

                # TODO: autre moyen. J aime pas.
                new_game = action.get('new_game')
                load_save_game = action.get('load_save_game')
                app_exit = action.get('app_exit')

                if app_exit:
                    if self.box_message:
                        self.box_message = {}
                    else:
                        break

                if new_game and not self.box_message:
                    # launch game
                    self.render_engine.reset_render_windows()
                    self.game = Game()
                    self.game.initialize()
                    self.app_states = AppStates.GAME

                elif load_save_game and not self.box_message:
                    try:
                        self.game = load_game('savegame')
                        # This is needed so the map & chars are fully rendered.
                        self.render_engine.reset_render_windows()
                        self.game.dungeon.current_map.fov_map = initialize_fov(self.game.dungeon.current_map)
                        self.game.full_recompute_fov()
                        self.app_states = AppStates.GAME
                    except FileNotFoundError:
                        self.box_message = {'header': 'File not found', 'options': []}

            elif self.app_states == AppStates.GAME:
                # empeche artefacts map lors d un changement etage
                if self.game.reset_game_windows:
                    self.render_engine.reset_render_windows(game_win=True)

                # render game
                self.render_engine.render_all(self.game, mouse)

                action = handle_keys(key, self.game.game_state)

                game_action = action.get('game')
                app_action = action.get('app')

                # play the game actions
                self.game.game_turn(game_action)

                exit = app_action.get('exit')
                if exit:
                    self.app_states = AppStates.MAIN_MENU

                fullscreen = app_action.get('fullscreen')
                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            else:
                print('app: state unknown : ', self.app_states)