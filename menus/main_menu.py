import tcod as libtcod
from game import Game
from states.app_states import AppStates
from data.data_loaders import load_game
from utils.fov_functions import initialize_fov
from menus.menu import MenuType, Menu


class MainMenu(Menu):
    def __init__(self, source):
        super().__init__(source)
        self.type = MenuType.GRAPHIC
        self.title = "CURSED FOREST"
        self.header = ""
        self.background_image = libtcod.image_load("menu_background.png")
        self._options = ["new game", "load game", "quit"]
        self.forced_width = 24

    def return_choice_result(self, string_choice):

        if string_choice == "quit":
            if self.source.box_message:
                self.source.box_message = {}
            else:
                self.source.quit_app = True

        if string_choice == "new game":
            self.source.render_engine.reset_render_windows()
            self.source.game = Game(self.source)
            self.source.game.initialize()
            self.source.app_states = AppStates.GAME
            self.source.current_menu = None

        elif string_choice == "load game":
            try:
                self.source.game = load_game("savegame")
                # This is needed so the map & chars are fully rendered.
                self.source.game.dungeon.current_map.fov_map = initialize_fov(
                    self.source.game.dungeon.current_map
                )
                self.source.game.full_recompute_fov()
                self.source.game.app = self.source  # On associe Game à App.
                self.source.app_states = AppStates.GAME
                self.source.reset_game_windows = True
                self.source.render_engine.reset_render_windows()
                self.source.current_menu = None
            except FileNotFoundError:
                self.source.current_menu = ErrorBox()


class ErrorBox(Menu):
    def __init__(self):
        super().__init__()
        self.header = """
        
        
        File not found
        
        
        """
        self.forced_width = 36
