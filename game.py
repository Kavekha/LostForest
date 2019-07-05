import tcod as libtcod
from bearlibterminal import terminal as blt

from config import app_config
from create_entities import create_fighting_entity
from utils.fov_functions import recompute_fov, discover_new_tiles
from handlers.event_handler import EventHandler
from data_loaders.data_loaders import save_game
from map_objects.dungeon import Dungeon
from utils.fov_functions import initialize_fov
from render_engine import RenderLayer


from systems.target_selection import Target


class Game:
    """
    orchestre les differents elements du jeu : carte, commandes, events.
    """

    def __init__(self, app):
        self.app = app

        # Fov options
        self.fov_algorithm = None
        self.fov_recompute = True

        # services
        self.events = None
        self.dungeon = None

        # menus / hacks
        self.current_menu = None

        self.player = None
        self.target_mode = False
        self.target = None

        self.round = 1

    def initialize(self):
        # recuperation de la config.
        # game_config = get_game_config()

        self.events = EventHandler(self)

        # gestion du fov.
        self.fov_algorithm = app_config.FOV_ALGORITHM

        # Creation du joueur.
        self.player = self.create_player()

        # Creation du dongeon
        self.dungeon = Dungeon(self, "Foret eternelle")
        self.dungeon.initialize()

        self.full_recompute_fov()

    def open_menu(self, menu):
        blt.layer(RenderLayer.BACKGROUND.value)
        blt.clear()
        blt.layer(RenderLayer.MENU.value)
        blt.clear()
        blt.refresh()
        self.current_menu = menu

    def close_menu(self):
        blt.layer(RenderLayer.BACKGROUND.value)
        blt.clear()
        blt.layer(RenderLayer.MENU.value)
        blt.clear()
        self.current_menu = None

    def activate_target_mode(self, target_source, target_type):
        self.close_menu()
        self.target_mode = True
        self.target = Target(self.player, self, target_source, target_type)

    def quit_target_mode(self):
        try:
            self.dungeon.current_map.remove_entity(self.target)
        except:
            # si n existe pas, tant mieux.
            pass
        self.target = None
        self.target_mode = False

    def recompute_fov(self):
        recompute_fov(
            self.dungeon.current_map.fov_map,
            self.player.x,
            self.player.y,
            self.player.fov_radius,
            self.player.light_walls,
            self.fov_algorithm,
        )

    def full_recompute_fov(self):
        blt.clear()
        game_map = self.dungeon.current_map
        game_map.fov_map = initialize_fov(game_map)
        self.recompute_fov()
        self.fov_recompute = True

    def create_player(self):
        player = create_fighting_entity(self, "player", 0, 0, player=True)
        return player

    def save_game(self):
        save_game(self)

    def game_turn(self):
        if self.player.round <= self.round:
            if self.target_mode:
                self.events.resolve_events()
            else:
                self.player_turn()
        else:
            self.enemy_turn()
            self.new_round()

    def new_round(self):
        self.round += 1
        self.save_game()

    def enemy_turn(self):
        for entity in self.dungeon.current_map.get_entities():
            if libtcod.map_is_in_fov(
                self.dungeon.current_map.fov_map, entity.x, entity.y
            ):
                if entity.ai:
                    entity.ai.take_turn(
                        self.dungeon.current_map, self.player, self.events
                    )
        self.events.resolve_events()

    def player_turn(self):
        self.fov_recompute = True
        self.events.resolve_events()
        if self.fov_recompute:
            self.recompute_fov()
            discover_new_tiles(self.dungeon.current_map)
