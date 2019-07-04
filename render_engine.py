import tcod as libtcod
from bearlibterminal import terminal as blt

from enum import Enum

from states.app_states import AppStates
from menus.menu import MenuType
from config import app_config


class RenderOrder(Enum):
    CORPSE = 1
    LANDMARK = 2
    ITEM = 3
    ACTOR = 4
    TARGET = 5


class Render:
    """
    responsabilité: Afficher les elements du jeu & interface.
    doit pouvoir être remplacé facilement par une autre librairie.
    """

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
        blt.open()
        blt.refresh()

    def render_app(self, app, mouse=None):
        if app.app_states == AppStates.MAIN_MENU:
            self._render_main_menu(app)
        elif app.app_states == AppStates.GAME:
            self._render_all(app, mouse)
        else:
            print("ERROR : Nothing to render.")

    def _render_main_menu(self, app):
        if app.current_menu:
            current_menu = app.current_menu
        else:
            current_menu = app.game.current_menu

        if current_menu:
            if current_menu.type == MenuType.GRAPHIC:
                self._main_menu(current_menu, self.screen_width, self.screen_height
                )
            elif current_menu.type == MenuType.STANDARD:
                self._menu(current_menu)

    def _menu(self, current_menu, width=None):
        if len(current_menu.options) > 26:
            raise ValueError("Cannot have a menu with more than 26 options.")

        header_height = 2
        height = len(current_menu.options) + header_height

        if not width:
            width = blt.state(blt.TK_WIDTH) // 6

        blt.printf(width, height, current_menu.header)

        topleft_x = blt.state(blt.TK_WIDTH) // 2 - width
        topleft_y = blt.state(blt.TK_HEIGHT) // 2 - height // 2

        y = header_height
        letter_index = ord("a")

        for option_text in current_menu.options:
            text = f'({chr(letter_index)}) - {option_text}'
            blt.printf(topleft_x, topleft_y + y, text)
            y += 1
            letter_index += 1
        blt.refresh()

    def _main_menu(self, current_menu_object, screen_width, screen_height):
        if current_menu_object.background_image:
            blt.set(f"U+E000: {current_menu_object.background_image}, resize=1260x800, resize-filter=nearest")
            blt.put(0, 0, 0xE000)  # Background

        title = app_config.APP_TITLE
        center = (blt.state(blt.TK_WIDTH) - len(title)) // 2
        blt.printf(center, blt.state(blt.TK_HEIGHT) // 2 - 4, title)

        title = app_config.VERSION
        center = (blt.state(blt.TK_WIDTH) - len(title)) // 2
        blt.printf(center, blt.state(blt.TK_HEIGHT) - 2, title)

        if current_menu_object.forced_width:
            width = current_menu_object.forced_width
        else:
            width = 24
        self._menu(current_menu_object, width)

    # Nous sommes In Game.
    def _render_all(self, app, mouse):
        game = app.game
        if game.fov_recompute:
            self._render_map(game)

        self._render_entities(game)

        # print message
        self._render_messages(game)
        # self._render_under_mouse(game, mouse)
        self._render_interface(game)
        self._render_dungeon_level(game)

        if game.current_menu:
            self._render_main_menu(app)

        game.fov_recompute = False
        blt.refresh()
        self._clear_all(game.dungeon.current_map.get_entities())

    def _render_interface(self, game):
        self._render_bar(
            1,
            1,
            "HP",
            game.player.fighter.hp,
            game.player.fighter.max_hp,
            libtcod.light_red,
            libtcod.darker_red,
        )

    def _render_under_mouse(self, game, mouse):
        blt.printf(self.panel, 1, '[color=grey]' + self._get_names_under_mouse(mouse, game))

    def _render_messages(self, game):
        messages = game.events.message_log.messages
        y = 1
        for message in messages:
            blt.printf(self.log_message_x, y, message.text)
            y += 1

    def _get_names_under_mouse(self, mouse, game):
        (x, y) = (mouse.cx, mouse.cy)

        names = [
            entity.name
            for entity in game.dungeon.current_map.get_entities()
            if entity.x == x
            and entity.y == y
            and libtcod.map_is_in_fov(
                game.dungeon.current_map.fov_map, entity.x, entity.y
            )
        ]
        names = ", ".join(names)

        return names.capitalize()

    def _render_dungeon_level(self, game):
        dungeon = game.dungeon
        blt.printf(1, 3, "{0} : {1}".format(dungeon.name, dungeon.current_floor))

    def _render_bar(self, x, y, name, value, maximum, bar_color, back_color):
        blt.printf(int(x + self.bar_width / 2), y, "{0}: {1}/{2}".format(name, value, maximum))

    def _render_map(self, game):
        game_map = game.dungeon.current_map
        terrain = game_map.get_terrain()
        width, height = game_map.get_map_sizes()
        for y in range(height):
            for x in range(width):
                visible = libtcod.map_is_in_fov(game_map.fov_map, x, y)
                current_tile = game_map.tiles[x][y]
                if visible:
                    if current_tile in (terrain.get('wall'),
                                        terrain.get('wall_explored'),
                                        terrain.get('indestructible_wall'),
                                        terrain.get('indestructible_wall_explored')
                                        ):
                        blt.printf(x, y, '[bkcolor=grey] [/bkcolor]')
                    elif current_tile in (terrain.get('ground'),
                                          terrain.get('ground_explored')
                                          ):
                        blt.printf(x, y, '[bkcolor=dark green] [/bkcolor]')
                elif current_tile.explored:
                    if current_tile in (terrain.get('wall'),
                                        terrain.get('wall_explored'),
                                        terrain.get('indestructible_wall'),
                                        terrain.get('indestructible_wall_explored')
                                        ):
                        blt.printf(x, y, '[bkcolor=dark grey] [/bkcolor]')
                    elif current_tile in (terrain.get('ground'),
                                          terrain.get('ground_explored')
                                          ):
                        blt.printf(x, y, '[bkcolor=darker green] [/bkcolor]')

    def _render_entities(self, game):
        game_map = game.dungeon.current_map
        entities_in_render_order = sorted(
            game_map.get_entities(), key=lambda x: x.render_order.value
        )
        for entity in entities_in_render_order:
            self._draw_entity(entity, game_map)

    def _draw_entity(self, entity, game_map):
        if libtcod.map_is_in_fov(game_map.fov_map, entity.x, entity.y) or \
                (entity.landmark and game_map.tiles[entity.x][entity.y].explored):
            blt.printf(entity.x, entity.y, entity.char)

    def _clear_all(self, entities):
        for entity in entities:
            self._clear_entity(entity)

    def _clear_entity(self, entity):
        # erase the character that represents this object
        blt.printf(entity.x, entity.y, ' ')
