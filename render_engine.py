import tcod as libtcod
from bearlibterminal import terminal as blt

from enum import Enum

from states.app_states import AppStates
from menus.menu import MenuType


class RenderLayer(Enum):
    MAP = 0 # floor & wall
    ENTITIES = 1    # Characters & items
    INTERFACE = 2
    BACKGROUND = 3  # Image
    MENU = 4


class RenderOrder(Enum):
    CORPSE = 1
    LANDMARK = 2
    ITEM = 3
    ACTOR = 4
    TARGET = 5


class Render:
    def __init__(self):
        self.has_menu = False

        blt.open()
        blt.refresh()

    def render_app(self, app):
        # que doit on mettre à jour?
        if self.has_menu != app.has_menu_open():
            self.has_menu = app.has_menu_open()
            if self.has_menu:
                self.render_menu(self.has_menu)

        blt.refresh()

    def render_menu(self, open_menu):
        print(f'j ai un menu que je n ai pas affiche jusqu a maintenant {open_menu}')
        # on efface les menus existants.
        self._clear_layer_background()
        self._clear_layer_menu()

        if open_menu.type == MenuType.GRAPHIC:
            self._render_graphic_menu(open_menu)
        self._render_standard_menu(open_menu)

    def _render_graphic_menu(self, open_menu):
        blt.layer(RenderLayer.BACKGROUND.value)
        blt.set(f"U+E000: {open_menu.background_image}, resize=1260x800, resize-filter=nearest")
        blt.put(0, 0, 0xE000)  # Background

    def _render_standard_menu(self, open_menu):
        blt.layer(RenderLayer.MENU.value)

        title = open_menu.title
        header = open_menu.header
        info = open_menu.info
        options = open_menu.display_options

        print(f'menu has {title}, {header}, {info}, {options}')

        x = blt.state(blt.TK_WIDTH) // 2
        y = blt.state(blt.TK_HEIGHT) // 2

        x_title = blt.state(blt.TK_WIDTH) // 2 - (len(title) // 2)
        y_title = blt.state(blt.TK_HEIGHT) // 4
        blt.printf(x_title, y_title, title)

        x_header = blt.state(blt.TK_WIDTH) // 2 - (len(header) // 2)
        y_header = blt.state(blt.TK_HEIGHT) // 3
        blt.printf(x_header, y_header, header)

        if options:
            x_option = blt.state(blt.TK_WIDTH) // 2 - (len(title) // 2)
            y_option = blt.state(blt.TK_HEIGHT) // 3 + 3
            for option in options:
                blt.printf(x_option, y_option, option)
                y_option += 1

        x_info = blt.state(blt.TK_WIDTH) // 2 - (len(info) // 2)
        y_info = blt.state(blt.TK_HEIGHT) - 2
        blt.printf(x_info, y_info, info)


    def _clear_layer_background(self):
        blt.layer(RenderLayer.BACKGROUND.value)
        blt.clear()

    def _clear_layer_menu(self):
        blt.layer(RenderLayer.MENU.value)
        blt.clear()


    '''
    game = app.game
    if game.fov_recompute:
        game.fov_recompute = False

        self._render_map(game)

    self._render_entities(game)

    self._render_interface(game)

    if game.current_menu:
        self._render_main_menu(app)

    game.fov_recompute = False
    blt.refresh()
    self._clear_all(game.dungeon.current_map.get_entities())
    '''


class OldRender:
    """
    responsabilité: Afficher les elements du jeu & interface.
    doit pouvoir être remplacé facilement par une autre librairie.
    """

    def __init__(self):
        blt.open()

        self.bar_width = blt.state(blt.TK_WIDTH) - (blt.state(blt.TK_WIDTH) // 4)
        self.panel_height = blt.state(blt.TK_HEIGHT) // 6
        self.panel_y = blt.state(blt.TK_WIDTH) - self.panel_height
        self.message_width = blt.state(blt.TK_WIDTH)- self.bar_width - 2
        self.message_height = self.panel_height - 1
        self.log_message_x = int(blt.state(blt.TK_WIDTH) / 3.5)
        self.log_message_width = blt.state(blt.TK_WIDTH) - self.bar_width - 2
        self.log_message_height = self.panel_height - 1

        blt.refresh()

    def render_app(self, app):
        if app.app_states == AppStates.MAIN_MENU:
            self._render_main_menu(app)
        elif app.app_states == AppStates.GAME:
            self._render_all(app)
        else:
            print("ERROR : Nothing to render.")

    def _render_main_menu(self, app):
        current_menu = app.current_menu if app.current_menu else app.game.current_menu

        if current_menu:
            self._main_menu(current_menu)

    def _menu(self, current_menu, width=None):
        blt.layer(RenderLayer.MENU.value)
        if len(current_menu.options) > 26:
            raise ValueError("Cannot have a menu with more than 26 options.")

        info = current_menu.info
        center = (blt.state(blt.TK_WIDTH) - len(info)) // 2
        blt.printf(center, blt.state(blt.TK_HEIGHT) - 2, info)

        header_height = 2
        height = len(current_menu.options) + header_height

        if not width:
            width = blt.state(blt.TK_WIDTH) // 6

        topleft_x = blt.state(blt.TK_WIDTH) // 2 - width
        topleft_y = blt.state(blt.TK_HEIGHT) // 2 - height // 2

        blt.printf(topleft_x, topleft_y - height, current_menu.header)

        y = header_height
        letter_index = ord("a")

        for option_text in current_menu.options:
            text = f'({chr(letter_index)}) - {option_text}'
            blt.printf(topleft_x, topleft_y + y, text)
            y += 1
            letter_index += 1

        blt.refresh()

    def _main_menu(self, current_menu_object):
        blt.layer(RenderLayer.BACKGROUND.value)
        if current_menu_object.background_image:
            blt.set(f"U+E000: {current_menu_object.background_image}, resize=1260x800, resize-filter=nearest")
            blt.put(0, 0, 0xE000)  # Background

        title = current_menu_object.title
        center = (blt.state(blt.TK_WIDTH) - len(title)) // 2
        blt.printf(center, blt.state(blt.TK_HEIGHT) // 2 - 4, title)

        if current_menu_object.forced_width:
            width = current_menu_object.forced_width
        else:
            width = 24
        self._menu(current_menu_object, width)

    # Nous sommes In Game.
    def _render_all(self, app):
        game = app.game
        if game.fov_recompute:
            game.fov_recompute = False

            self._render_map(game)

        self._render_entities(game)

        self._render_interface(game)

        if game.current_menu:
            self._render_main_menu(app)

        game.fov_recompute = False
        blt.refresh()
        self._clear_all(game.dungeon.current_map.get_entities())

    def _render_interface(self, game):
        blt.layer(RenderLayer.INTERFACE.value)
        self._render_bar(
            1,
            blt.state(blt.TK_HEIGHT) - blt.state(blt.TK_HEIGHT) // 10,
            "HP",
            game.player.fighter.hp,
            game.player.fighter.max_hp,
            libtcod.light_red,
            libtcod.darker_red,
        )
        self._render_messages(game)
        self._render_dungeon_name(game)
        blt.refresh()

    def _render_bar(self, x, y, name, value, maximum, bar_color, back_color):
        blt.printf(x, y, "{0}: {1}/{2}".format(name, value, maximum))

    def _render_messages(self, game):
        blt.layer(RenderLayer.INTERFACE.value)
        messages = game.events.message_log.messages
        x = self.log_message_x
        y = blt.state(blt.TK_HEIGHT) - self.panel_height
        for message in messages:
            blt.printf(x, y, message.text)
            y += 1

    def _render_dungeon_name(self, game):
        dungeon = game.dungeon
        y = blt.state(blt.TK_HEIGHT) - self.panel_height
        blt.printf(1, y, "{0} : {1}".format(dungeon.name, dungeon.current_floor))

    def _render_map(self, game):
        blt.layer(RenderLayer.MAP.value)
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
                        blt.printf(x, y, f'[bkcolor={game_map.colors.get("light_wall")}] [/bkcolor]')
                    elif current_tile in (terrain.get('ground'),
                                          terrain.get('ground_explored')
                                          ):
                        blt.printf(x, y, f'[bkcolor={game_map.colors.get("light_ground")}] [/bkcolor]')
                elif current_tile.explored:
                    if current_tile in (terrain.get('wall'),
                                        terrain.get('wall_explored'),
                                        terrain.get('indestructible_wall'),
                                        terrain.get('indestructible_wall_explored')
                                        ):
                        blt.printf(x, y, f'[bkcolor={game_map.colors.get("dark_wall")}] [/bkcolor]')
                    elif current_tile in (terrain.get('ground'),
                                          terrain.get('ground_explored')
                                          ):
                        blt.printf(x, y, f'[bkcolor={game_map.colors.get("dark_ground")}] [/bkcolor]')

    def _render_entities(self, game):
        blt.layer(RenderLayer.ENTITIES.value)
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
        blt.layer(RenderLayer.ENTITIES.value)
        for entity in entities:
            self._clear_entity(entity)

        blt.layer(RenderLayer.INTERFACE.value)
        blt.clear_area(0, 0, blt.state(blt.TK_WIDTH, blt.TK_HEIGHT))

        blt.layer(RenderLayer.MENU.value)
        blt.clear_area(0, 0, blt.state(blt.TK_WIDTH, blt.TK_HEIGHT))

    def _clear_entity(self, entity):
        # erase the character that represents this object
        blt.clear_area(entity.x, entity.y, entity.x, entity.y)

