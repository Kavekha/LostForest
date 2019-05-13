import libtcodpy as libtcod
from utils.fov_functions import recompute_fov
from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


class Render:
    '''
    responsabilité: Afficher les elements du jeu & interface.
    doit pouvoir être remplacé facilement par une autre librairie.
    '''
    def __init__(self, screen_width=80, screen_height=50):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._initialize_render()
        self.game_window = None

    def _initialize_render(self):
        libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(self.screen_width, self.screen_height, 'Lost Forest', False)

        # la fenetre dans lequel le jeu sera affiché.
        self.game_window = libtcod.console_new(self.screen_width, self.screen_height)

    def render_all(self, game):
        # doit-on recalculer le field of vision? # TODO : Est-ce vraiment responsabilité du render all de calculer FOV?
        if game.fov_recompute:
            recompute_fov(game.map.fov_map, game.player.x, game.player.y, game.player.fov_radius,
                          game.player.light_walls, game.fov_algorithm)
            self._render_map(game.map)

        self._render_entities(game.map.entities, game.map.fov_map)

        self._render_interface(game)

        libtcod.console_blit(self.game_window, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
        libtcod.console_flush()
        self._clear_all(game.map.entities)
        game.fov_recompute = False

    def _render_interface(self, game):
        libtcod.console_set_default_foreground(self.game_window, libtcod.white)
        libtcod.console_print_ex(self.game_window, 1, self.screen_height - 2, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'HP: {0:02}/{1:02}'.format(game.player.fighter.hp, game.player.fighter.max_hp))

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
