from config import app_config
from game import Game
from data_loaders.data_loaders import load_game, refresh_at_load
from menus.menu import MenuType, Menu
from menus.language_menu import LanguageMenu
from data_loaders.localization import Texts


class MainMenu(Menu):
    def __init__(self, source):
        super().__init__(source)
        self.type = MenuType.GRAPHIC
        self.title = app_config.APP_TITLE
        self.header = ""
        self.info = app_config.VERSION
        self.background_image = './medias/creepy_wood.jpg'
        self.display_options = [Texts.get_text('MAIN_MENU_NEW_GAME'),
                                Texts.get_text('MAIN_MENU_LOAD_GAME'),
                                Texts.get_text('MAIN_MENU_LANGUAGES'),
                                Texts.get_text('MAIN_MENU_QUIT')]
        self._options = ["new game", "load game", "languages", "quit"]
        self.forced_width = 24

    def return_choice_result(self, string_choice):

        if string_choice == "quit":
            self.source.exit_window()

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

        elif string_choice == 'languages':
            self.source.open_menu(LanguageMenu(self.source))


class ErrorBox(Menu):
    def __init__(self):
        super().__init__()
        self.header = """
        
        
        File not found
        
        
        """
        self.forced_width = 36
