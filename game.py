from data.create_entities import create_fighting_entity
from config.config import get_game_config
from utils.fov_functions import recompute_fov, discover_new_tiles
from states.game_states import GameStates
from handlers.event_handler import EventHandler
from data.data_loaders import save_game
from map_objects.dungeon import Dungeon
from utils.fov_functions import initialize_fov
import libtcodpy as libtcod


class Game:
    '''
    orchestre les differents elements du jeu : carte, commandes, events.
    '''
    def __init__(self):
        self.events = None
        self.fov_algorithm = None
        self.fov_recompute = True
        self.player = None
        self.dungeon = None
        self.game_state = None
        self.previous_game_state = GameStates.PLAYERS_TURN
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
        self.game_state = GameStates.PLAYERS_TURN

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

    def game_turn(self, player_action):
        if self.player.round <= self.round:
            self.player_turn(player_action)
        else:
            self.enemy_turn()
            self.new_round()

    def new_round(self):
        self.round += 1
        print('Current round is now ', self.round)

    def enemy_turn(self):
        for entity in self.dungeon.current_map.entities:
            if libtcod.map_is_in_fov(self.dungeon.current_map.fov_map, entity.x, entity.y):
                if entity.ai:
                    entity.ai.take_turn(self.dungeon.current_map, self.player, self.events)
        self.events.resolve_events()
        save_game(self)

    def player_turn(self, player_action):
        self.fov_recompute = True

        self.events.resolve_events()
        if self.fov_recompute:
            self.recompute_fov()
            discover_new_tiles(self.dungeon.current_map)
        save_game(self)

        show_inventory = player_action.get('show_inventory')
        exit = player_action.get('exit')
        game_option_choice = player_action.get('game_option_choice')

        if show_inventory:
            self.previous_game_state = self.game_state
            self.game_state = GameStates.SHOW_INVENTORY

        # Si un element d'une liste a été choisi, qu'on est pas mort et que le nb est inferieur au nb items
        # dans l'inventaire.
        if game_option_choice is not None \
                and self.previous_game_state != GameStates.PLAYER_DEAD \
                and game_option_choice < len(self.player.inventory.items):
            item = self.player.inventory.items[game_option_choice]
            self.player.inventory.use(item)

        if exit:
            if self.game_state == GameStates.SHOW_INVENTORY:
                self.game_state = self.previous_game_state
                self.previous_game_state = None
            else:
                # TODO: Ask for leave the game or not
                save_game(self)







