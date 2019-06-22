from menus.menu import Menu
from systems.localization import Texts


class LanguageMenu(Menu):
    def __init__(self, source):
        super().__init__(source)
        self.source = source
        self.header = Texts.get_text('MENU_CHOOSE_LANGUAGE')
        self.display_options = list(Texts.get_available_languages())
        self._options = list(Texts.get_available_languages())
        self.forced_width = 24

    def receive_option_choice(self, choice):
        if choice < len(self._options):
            string_choice = self._options[choice]
            self.return_choice_result(string_choice)

    def return_choice_result(self, string_choice):
        Texts.set_language(string_choice)
        self.update_options()

    def update_options(self):
        self.source.current_menu = LanguageMenu(self.source)
