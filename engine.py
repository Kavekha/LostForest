import libtcodpy as libtcod
from config.config import get_app_config
from render_engine import Render
from states.app_states import AppStates
from systems.commands import CommandController
from handlers.input_handlers import InputHandler
from menus.main_menu import MainMenu


class App:
    def __init__(self):
        # app config
        config = get_app_config()

        # input handler
        self.command_controller = CommandController()
        self.input_handler = InputHandler(self, self.command_controller)

        # render engine
        screen_width = config['screen_width']
        screen_height = config['screen_height']
        bar_width = config['bar_width']
        panel_height = config['panel_height']
        self.render_engine = Render(screen_width, screen_height, bar_width, panel_height)

        self.app_states = None
        self.box_message = None
        self.current_menu = None
        self.quit_app = False

        self.game = None

    def run(self):
        # initialize controls.
        key = libtcod.Key()
        mouse = libtcod.Mouse()

        self.app_states = AppStates.MAIN_MENU
        self.current_menu = MainMenu(self)

        # main loop
        while not libtcod.console_is_window_closed():
            # check key / mouse event
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

            self.render_engine.render_app(self, mouse)

            if self.game and self.game.reset_game_windows:
                self.render_engine.reset_render_windows()

            self.input_handler.press(key)

            if self.app_states == AppStates.GAME:
                self.game.game_turn()

            if self.quit_app:
                break

    def exit_window(self):
        if self.app_states == AppStates.GAME:
            if self.game.current_menu:
                self.game.current_menu = None
            else:
                self.app_states = AppStates.MAIN_MENU
                self.current_menu = MainMenu(self)
        elif self.app_states == AppStates.MAIN_MENU:
            if isinstance(self.current_menu, MainMenu):
                self.quit_app = True
            else:
                self.current_menu = MainMenu(self)

    def full_screen(self):
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
