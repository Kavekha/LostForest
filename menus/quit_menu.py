from menus.menu import Menu
from config.constants import ConstTexts
from systems.commands import ExitWindow


class QuitMenu(Menu):
    def __init__(self, app):
        super().__init__(app)
        self.header = ConstTexts.QUIT_GAME_MENU_HEADER
        self._options = [ConstTexts.YES_MENU, ConstTexts.NO_MENU]
        self.back_to_main = False

    def return_choice_result(self, string_choice):
        if string_choice == ConstTexts.YES_MENU:
            self.back_to_main = True
        self.source.command_controller.execute(ExitWindow(self.source))
