from menus.menu import Menu, MenuType
import tcod as libtcod
from data_loaders.localization import Texts


class VictoryMenu(Menu):
    def __init__(self):
        super().__init__()
        self.type = MenuType.GRAPHIC
        self.title = Texts.get_text('VICTORY_1_TITLE')
        self.header = ("""
        
"""
                       + Texts.get_text('VICTORY_1_PART_1')
                       + ' \n'
                       + Texts.get_text('VICTORY_1_PART_2')
                       + '\n'
                       + """

"""
                       )
        self.background_image = libtcod.image_load("menu_background.png")
        self._options = []
        self.forced_width = 48
        self.back_to_main = True
