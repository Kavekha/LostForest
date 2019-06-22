import tcod as libtcod

from game import Game
from data.data_loaders import load_game, refresh_at_load
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
            self.source.game = Game(self.source)
            self.source.game.initialize()
            refresh_at_load(self.source)

        elif string_choice == "load game":
            try:
                self.source.game = load_game("savegame")
                refresh_at_load(self.source)
            except FileNotFoundError:
                self.source.current_menu = ErrorBox()


class ErrorBox(Menu):
    def __init__(self):
        super().__init__()
        self.header = """
        
        
        File not found
        
        
        """
        self.forced_width = 36
