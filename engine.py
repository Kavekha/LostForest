from bearlibterminal import terminal as blt

from render_engine import Render, RenderLayer
from states.app_states import AppStates
from systems.commands import CommandController
from handlers.input_handlers import InputHandler
from menus.main_menu import MainMenu
from menus.quit_menu import QuitMenu


class App:
    def __init__(self):
        # input handler
        self.command_controller = CommandController()
        self.input_handler = InputHandler(self, self.command_controller)

        # render engine
        self.render_engine = Render()

        self.app_states = None
        self.current_menu = None
        self.quit_app = False
        self.game = None

    def run(self):
        self.app_states = AppStates.MAIN_MENU
        self.current_menu = MainMenu(self)

        while True:
            if blt.has_input():
                key = blt.read()

                self.input_handler.press(key)

            self.render_engine.render_app(self)

            if self.app_states == AppStates.GAME:
                self.game.game_turn()

            if self.quit_app:
                break

    def open_menu(self, menu):
        blt.layer(RenderLayer.BACKGROUND.value)
        blt.clear()
        blt.layer(RenderLayer.MENU.value)
        blt.clear()
        blt.refresh()
        self.current_menu = menu

    def exit_window(self):
        # Menus in game
        if self.app_states == AppStates.GAME:
            if self.game.target_mode:
                self.game.quit_target_mode()

            # Si pas de menu, on propose de quitter
            elif not self.game.current_menu:
                self.game.current_menu = QuitMenu(self)
            # Si menu, avec back to main quand on exit
            elif self.game.current_menu.back_to_main:
                self.app_states = AppStates.MAIN_MENU
                self.current_menu = MainMenu(self)
                self.game.close_menu()
            else:
                # on quitte le menu actuel pour revenir au jeu
                self.game.close_menu()

        elif self.app_states == AppStates.MAIN_MENU:
            # Je suis dans le main menu, je quitte l'appli
            if isinstance(self.current_menu, MainMenu):
                self.quit_app = True
            else:
                self.current_menu = MainMenu(self)
        blt.clear()
        blt.refresh()

    def full_screen(self):
        raise NotImplementedError
