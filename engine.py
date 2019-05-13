import libtcodpy as libtcod
from config.config import get_app_config
from input_handlers import handle_keys
from render_engine import Render
from game import Game


class App:
    def __init__(self):
        # app config
        config = get_app_config()
        screen_width = config['screen_width']
        screen_height = config['screen_height']

        # render engine
        self.render_engine = Render(screen_width, screen_height)

        # launch game
        self.game = Game()

    def run(self):
        # initialize controls.
        key = libtcod.Key()
        mouse = libtcod.Mouse()

        # main loop
        while not libtcod.console_is_window_closed():
            # check key / mouse event
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

            # render game
            self.render_engine.render_all(self.game)

            # get player action for both app & game
            action = handle_keys(key)
            game_action = action.get('game')
            app_action = action.get('app')

            # play the game actions
            self.game.game_turn(game_action)

            exit = app_action.get('exit')
            if exit:
                return True

            fullscreen = app_action.get('fullscreen')
            if fullscreen:
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
