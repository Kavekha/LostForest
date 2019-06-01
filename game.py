from data.create_entities import create_fighting_entity
from config.config import get_game_config
from utils.fov_functions import recompute_fov, discover_new_tiles
from handlers.event_handler import EventHandler
from data.data_loaders import save_game
from map_objects.dungeon import Dungeon
from utils.fov_functions import initialize_fov
import libtcodpy as libtcod


class Game:
    '''
    orchestre les differents elements du jeu : carte, commandes, events.
    '''
    def __init__(self, app):
        self.app = app
        self.events = None
        self.fov_algorithm = None
        self.fov_recompute = True
        self.player = None
        self.dungeon = None
        self.current_menu = None
        self.round = 1

    def initialize(self):
        # recuperation de la config.
        game_config = get_game_config()

        self.events = EventHandler(self)

        # gestion du fov.
        self.fov_algorithm = game_config['fov_algorithm']
        self.fov_recompute = True
        self.reset_game_windows = False # Pour contré les artefacts lors d'un changement d'etage.

        # Creation du joueur.
        self.player = self.create_player()

        # Creation du dongeon
        self.dungeon = Dungeon(self, 'Foret eternelle')
        self.dungeon.initialize()

        self.full_recompute_fov()

    def recompute_fov(self):
        recompute_fov(self.dungeon.current_map.fov_map, self.player.x, self.player.y, self.player.fov_radius,
                      self.player.light_walls, self.fov_algorithm)

    def full_recompute_fov(self):
        game_map = self.dungeon.current_map
        game_map.fov_map = initialize_fov(game_map)
        self.recompute_fov()
        self.fov_recompute = True

    def create_player(self):
        player = create_fighting_entity(self, 'player', 0, 0, player=True)
        return player

    def save_game(self):
        save_game(self)

    def game_turn(self):
        if self.player.round <= self.round:
            self.player_turn()
        else:
            self.enemy_turn()
            self.new_round()

    def new_round(self):
        self.round += 1
        print('--- Round {}'.format(self.round))
        self.save_game()

    def enemy_turn(self):
        for entity in self.dungeon.current_map.entities:
            if libtcod.map_is_in_fov(self.dungeon.current_map.fov_map, entity.x, entity.y):
                if entity.ai:
                    entity.ai.take_turn(self.dungeon.current_map, self.player, self.events)
        self.events.resolve_events()

    def player_turn(self):
        self.fov_recompute = True

        self.events.resolve_events()
        if self.fov_recompute:
            self.recompute_fov()
            discover_new_tiles(self.dungeon.current_map)
