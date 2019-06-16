from menus.menu import Menu, MenuType
import tcod as libtcod


class VictoryMenu(Menu):
    def __init__(self):
        super().__init__()
        self.type = MenuType.GRAPHIC
        self.title = "VICTORY"
        self.header = """
        
You are now out of the woods, out of danger.
Behind you, the Cursed Forest still grows.

        """
        self.background_image = libtcod.image_load("menu_background.png")
        self._options = []
        self.forced_width = 48
        self.back_to_main = True
