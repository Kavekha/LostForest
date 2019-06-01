from enum import Enum


class MenuType(Enum):
    GRAPHIC = 0
    STANDARD = 0


class Menu:
    def __init__(self, source=None):
        self.source = source
        self.type = MenuType.STANDARD
        self.title = ''     # Graphic only
        self.header = ''
        self.background_image = None    # libtcod.image_load('menu_background.png')
        self._options = []
        self.display_options = None
        self.forced_width = None    # To force width in Render menu
        self.back_to_main = False   # Si True : quitter ce menu rammene au MainScreen / APP (Victory / Death)

    @property
    def options(self):
        if self.display_options:
            return self.display_options
        else:
            return self._options

    def receive_option_choice(self, choice):
        if choice >= len(self._options):
            print('menu:option choice: no choice : option available : ', self.options)
        else:
            string_choice = self._options[choice]
            self.return_choice_result(string_choice)

    def return_choice_result(self, string_choice):
        raise NotImplementedError

    def update_options(self):
        raise NotImplementedError
