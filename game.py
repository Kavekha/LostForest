import libtcodpy as libtcod

from map_objects.map import GameMap
from entities import Entity
from config.config import get_game_config
from utils.fov_functions import recompute_fov, discover_new_tiles
from states.game_states import GameStates
from components.fighter import Fighter
from data.playable_archetypes import get_player_stats
from event_handler import EventHandler
from render_engine import RenderOrder


class Game:
    '''
    orchestre les differents elements du jeu : carte, commandes, events.
    '''
    def __init__(self):
        # recuperation de la config.
        game_config = get_game_config()

        self.events = EventHandler(self)

        # gestion du fov.
        self.fov_algorithm = game_config['fov_algorithm']
        self.fov_recompute = True

        # Creation de la map du debut & creation joueur & son placement.
        self.map = GameMap(self, 'standard_map')
        self.player = self.create_player()
        self.map.add_player(self.player)
        self.map.generate_map(self)
        recompute_fov(self.map.fov_map, self.player.x, self.player.y, self.player.fov_radius, self.player.light_walls,
                      self.fov_algorithm)

        self.game_state = GameStates.PLAYERS_TURN

    # TODO : Est ce qu'on a besoin d'avoir la position à la creation? Ne peut on pas la donner lors de l'arrivée sur map
    def create_player(self):
        player_stats = get_player_stats('base_player')
        if player_stats:
            fighter_component = Fighter(hp=player_stats['hp'])

            player = Entity(self,
                            int(self.map.width / 2), int(self.map.height / 2),
                            '@', libtcod.white, 'Player', blocks=True,
                            fighter=fighter_component,
                            render_order=RenderOrder.ACTOR)
            return player
        else:
            return None

    def game_turn(self, player_action):
        # TODO: Tour selon une timeline.
        if self.game_state == GameStates.PLAYERS_TURN:
            self.player_turn(player_action)
        elif self.game_state == GameStates.ENEMY_TURN:
            self.enemy_turn()
        elif self.game_state == GameStates.PLAYER_DEAD:
            pass

        # event resolution
        self.events.resolve_events()

        # Si une action a devoilé de nouvelles tiles, on les considère comme discovered.
        # TODO Est ce que cela doit etre dans le game turn?
        if self.fov_recompute:
            recompute_fov(self.map.fov_map, self.player.x, self.player.y, self.player.fov_radius,
                          self.player.light_walls, self.fov_algorithm)
            discover_new_tiles(self.map)

    def enemy_turn(self):
        for entity in self.map.entities:
            if entity.ai:
                entity.ai.take_turn(self.map, self.player, self.events)
        self.enemy_end_turn()

    def enemy_end_turn(self):
        self.game_state = GameStates.PLAYERS_TURN

    def player_turn(self, player_action):
        # on recupere les actions faites par le joueur pour les gerer.
        move = player_action.get('move')

        if move:
            # le joueur tente de se deplacer vers une case.
            # Si vide : ok
            # si wall : refusé
            # si entité : interaction
            dx, dy = move
            self.player.try_to_move(dx, dy)
            self.fov_recompute = True
            self.player_end_turn()

    def player_end_turn(self):
        self.game_state = GameStates.ENEMY_TURN





