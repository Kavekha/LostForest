from menus.menu import Menu
from data_loaders.localization import Texts
from systems.commands import ExitWindow


class QuitMenu(Menu):
    def __init__(self, app):
        super().__init__(app)
        self.header = Texts.get_text('QUIT_GAME_MENU_HEADER')
        self._options = [Texts.get_text('YES_ANSWER'), Texts.get_text('NO_ANSWER')]
        self.back_to_main = False

    def return_choice_result(self, string_choice):
        if string_choice == Texts.get_text('YES_ANSWER'):
            self.back_to_main = True
        self.source.command_controller.execute(ExitWindow(self.source))
