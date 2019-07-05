import tcod as libtcod
from bearlibterminal import terminal as blt

from enum import Enum

from states.app_states import AppStates
from menus.menu import MenuType
from utils.text_functions import get_biggest_line_len


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
        self.menu_title_placement = (
                blt.state(blt.TK_WIDTH) // 2,
                blt.state(blt.TK_HEIGHT) // 2 - 3
        )
        self.menu_header_placement = (
                blt.state(blt.TK_WIDTH) // 2,
                blt.state(blt.TK_HEIGHT) // 2
        )
        self.menu_info_placement = (
            blt.state(blt.TK_WIDTH) // 2,
            blt.state(blt.TK_HEIGHT) - 2
        )
        self.menu_options_placement = (
            blt.state(blt.TK_WIDTH) // 2,
            blt.state(blt.TK_HEIGHT) // 2 + 3
        )
        self.panel = (
            1,
            blt.state(blt.TK_HEIGHT) - 7
        )
        self.log_panel = (
            int(blt.state(blt.TK_WIDTH) / 4),
            blt.state(blt.TK_HEIGHT) - 7
        )

        blt.refresh()


    def get_menu_position(self, position):
        position = position.lower()
        x = blt.state(blt.TK_WIDTH) // 2
        y = 0

        if position == 'center':
            y = blt.state(blt.TK_HEIGHT) // 2
        elif position == 'bottom':
            y = blt.state(blt.TK_HEIGHT)
        elif position == 'top':
            y = 0
        elif position == 'midbottom':
            y = blt.state(blt.TK_HEIGHT) - blt.state(blt.TK_HEIGHT) // 6
        elif position == "midtop":
            y = blt.state(blt.TK_HEIGHT) // 6

        return x, y

    def render_app(self, app):

        # que doit on mettre à jour?
        if self.has_menu != app.has_menu_open():
            self.has_menu = app.has_menu_open()
            if self.has_menu:
                self.render_menu(self.has_menu)

            blt.refresh()

        if app.game:
            game = app.game
            if game.fov_recompute:
                game.fov_recompute = False
                self.render_map(game)

            self.render_entities(game)

            self.render_interface(game)

            blt.refresh()
            self._clear_all(game.dungeon.current_map.get_entities())

    def render_map(self, game):
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
        try:
            position = self.get_menu_position(open_menu.position)
        except AttributeError:
            print('menu does not have position. Use default.')
            position = None

        if position:
            x, y = position
        else:
            x, y = self.menu_title_placement
        x = (blt.state(blt.TK_WIDTH) - len(title)) // 2
        blt.printf(x, y, title)

        if position:
            x, y = position
        else:
            x, y = self.menu_header_placement
        x = (blt.state(blt.TK_WIDTH) - get_biggest_line_len(header)) // 2
        blt.printf(x, y, header)
        print(f'header len is {header}')
        print(f'lines in header is {get_biggest_line_len(header)}')

        if position:
            x, y = position
        else:
            x, y = self.menu_info_placement
        x = (blt.state(blt.TK_WIDTH) - len(info)) // 2
        blt.printf(x - (len(info) // 2), y, info)

        if options:
            letter_index = ord("a")
            if position:
                x, y = position
            else:
                x, y = self.menu_options_placement
            bigger_len = get_biggest_line_len(options)

            x = (blt.state(blt.TK_WIDTH) - bigger_len) // 2
            for option in options:
                text = f'{chr(letter_index)} - {option}'
                blt.printf(x, y, text)
                y += 1
                letter_index += 1

    def _clear_area(self):
        blt.clear_area(0, 0, blt.state(blt.TK_WIDTH), blt.state(blt.TK_HEIGHT))

    def _clear_layer_background(self):
        blt.layer(RenderLayer.BACKGROUND.value)
        self._clear_area()

    def _clear_layer_menu(self):
        blt.layer(RenderLayer.MENU.value)
        self._clear_area()

    def _clear_layer_interface(self):
        blt.layer(RenderLayer.INTERFACE.value)
        self._clear_area()

    def render_interface(self, game):
        blt.layer(RenderLayer.INTERFACE.value)
        self._clear_layer_interface()
        x, y = self.panel
        self._render_bar(
            x,
            y,
            "HP",
            game.player.fighter.hp,
            game.player.fighter.max_hp
        )
        self._render_messages(game)
        self._render_dungeon_name(game)
        blt.refresh()

    def _render_bar(self, x, y, name, value, maximum):
        text = f"{name}: {value}/{maximum}"
        blt.printf(x, y, text)

    def _render_messages(self, game):
        messages = game.events.message_log.messages
        x, y = self.log_panel
        for message in messages:
            blt.printf(x, y, message.text)
            y += 1

    def _render_dungeon_name(self, game):
        text = f'{game.dungeon.name}:{game.dungeon.current_floor}'
        x, y = self.panel
        y += 1
        blt.printf(x, y, text)

    def render_entities(self, game):
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
