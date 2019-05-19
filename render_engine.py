import libtcodpy as libtcod
from states.game_states import GameStates
from enum import Enum
from menus.main_menu import menu


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


class Render:
    '''
    responsabilité: Afficher les elements du jeu & interface.
    doit pouvoir être remplacé facilement par une autre librairie.
    '''
    def __init__(self, screen_width=80, screen_height=50, bar_width=20, panel_height=7):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.panel_height = panel_height
        self.bar_width = bar_width
        self.panel_y = screen_height - panel_height
        self.message_x = bar_width + 2
        self.message_width = screen_width - bar_width - 2
        self.message_height = panel_height - 1
        self.log_message_x = bar_width + 2
        self.log_message_width = screen_width - bar_width - 2
        self.log_message_height = panel_height - 1

        self._initialize_render()

    def _initialize_render(self):
        libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(self.screen_width, self.screen_height, 'Lost Forest', False)

        # la fenetre dans lequel le jeu sera affiché.
        self.game_window = libtcod.console_new(self.screen_width, self.screen_height)
        self.panel = libtcod.console_new(self.screen_width, self.panel_height)
        self.menu_window = libtcod.console_new(self.screen_width, self.screen_height)

    def render_all(self, game, mouse):

        # doit-on recalculer le field of vision? # TODO : Est-ce vraiment responsabilité du render all de calculer FOV?
        # if game.fov_recompute:
        self._render_map(game.map)
        if game.fov_recompute:
            print('self menu windows : ', self.menu_window)
            print('self game windows : ', self.game_window)
            print('self panel window : ', self.panel)

        libtcod.console_set_default_background(self.menu_window, libtcod.black)
        libtcod.console_clear(self.menu_window)

        self._render_entities(game.map.entities, game.map.fov_map)

        libtcod.console_blit(self.game_window, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)

        libtcod.console_set_default_background(self.panel, libtcod.black)
        libtcod.console_clear(self.panel)

        # print message
        self._render_messages(game)
        self._render_under_mouse(game, mouse)
        self._render_interface(game)
        libtcod.console_blit(self.panel, 0, 0, self.screen_width, self.panel_height, 0, 0, self.panel_y)

        # if menu

        if game.game_state == GameStates.SHOW_INVENTORY:
            self._render_menu(game)

        game.fov_recompute = False
        libtcod.console_flush()
        self._clear_all(game.map.entities)

    def menu(self, con, header, options, width, screen_width, screen_height):
        if len(options) > 26:
            raise ValueError('Cannot have a menu with more than 26 options.')

        # calculate total height for the header (after auto-wrap) and one line per option
        header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
        height = len(options) + header_height

        # create an off-screen console that represents the menu's window
        self.menu_window = libtcod.console_new(self.screen_width, self.screen_height)

        # print the header, with auto-wrap
        libtcod.console_set_default_foreground(self.menu_window, libtcod.white)
        libtcod.console_print_rect_ex(self.menu_window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

        # print all the options
        y = header_height
        letter_index = ord('a')

        for option_text in options:
            text = '(' + chr(letter_index) + ') ' + option_text
            libtcod.console_print_ex(self.menu_window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1

        # blit the contents of "window" to the root console
        x = int(screen_width / 2 - width / 2)
        y = int(screen_height / 2 - height / 2)
        libtcod.console_blit(self.menu_window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    def _render_interface(self, game):
        self.render_bar(1, 1, 'HP', game.player.fighter.hp, game.player.fighter.max_hp,
                   libtcod.light_red, libtcod.darker_red)

    def _render_menu(self, game):
        header, options = game.player.inventory.menu_options()
        self.menu(self.game_window, header, options, int(self.screen_width / 1.5), self.screen_width, self.screen_height)

    def _render_under_mouse(self, game, mouse):
        libtcod.console_set_default_foreground(self.panel, libtcod.light_gray)
        libtcod.console_print_ex(self.panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                                 self.get_names_under_mouse(mouse, game))

    def _render_messages(self, game):
        messages = game.events.message_log.messages
        y = 1
        for message in messages:
            libtcod.console_set_default_foreground(self.panel, message.color)
            libtcod.console_print_ex(self.panel, self.log_message_x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
            y += 1

    def get_names_under_mouse(self, mouse, game):
        (x, y) = (mouse.cx, mouse.cy)

        names = [entity.name for entity in game.map.entities
                 if entity.x == x and entity.y == y and libtcod.map_is_in_fov(game.map.fov_map, entity.x, entity.y)]
        names = ', '.join(names)

        return names.capitalize()

    def render_bar(self, x, y, name, value, maximum, bar_color, back_color):
        current_bar_width = int(float(value) / maximum * self.bar_width)

        libtcod.console_set_default_background(self.panel, back_color)
        libtcod.console_rect(self.panel, x, y, self.bar_width, 1, False, libtcod.BKGND_SCREEN)

        libtcod.console_set_default_background(self.panel, bar_color)
        if current_bar_width > 0:
            libtcod.console_rect(self.panel, x, y, current_bar_width, 1, False, libtcod.BKGND_SCREEN)

        libtcod.console_set_default_foreground(self.panel, libtcod.white)
        libtcod.console_print_ex(self.panel, int(x + self.bar_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 '{0}: {1}/{2}'.format(name, value, maximum))

    def _render_map(self, game_map):
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(game_map.fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_set_char_background(self.game_window, x, y, game_map.colors.get('light_wall'),
                                                            libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(self.game_window, x, y, game_map.colors.get('light_ground'),
                                                            libtcod.BKGND_SET)
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(self.game_window, x, y, game_map.colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(self.game_window, x, y, game_map.colors.get('dark_ground'), libtcod.BKGND_SET)

    def _render_entities(self, entities, fov_map):
        entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
        for entity in entities_in_render_order:
            self._draw_entity(entity, fov_map)

    def _draw_entity(self, entity, fov_map):
        if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            libtcod.console_set_default_foreground(self.game_window, entity.color)
            libtcod.console_put_char(self.game_window, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

    def _clear_all(self, entities):
        for entity in entities:
            self._clear_entity(entity)

    def _clear_entity(self, entity):
        # erase the character that represents this object
        libtcod.console_put_char(self.game_window, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
