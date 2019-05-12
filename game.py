from map_objects.map import GameMap
from entities import Entity, get_blocking_entities_at_location
import libtcodpy as libtcod
from data.config import get_game_config
from utils.fov_functions import recompute_fov, discover_new_tiles
from states.game_states import GameStates


class Game:
    '''
    gère les elements du jeu en lui-même : la carte, le combat, etc.
    '''
    def __init__(self):
        # recuperation de la config.
        game_config = get_game_config()

        # gestion du fov.
        # TODO : Aujourd'hui partagé avec Render, qui recalcule la FOV. Pas vraiment sa responsabilité.
        self.fov_algorithm = game_config['fov_algorithm']
        self.fov_recompute = True

        # Creation de la map du debut & creation joueur & son placement.
        self.map = GameMap('standard_map')
        self.player = Entity(int(self.map.width / 2), int(self.map.height / 2), '@',
                             libtcod.white, 'Player', blocks=True)
        self.map.add_player(self.player)
        self.map.generate_map(self)
        recompute_fov(self.map.fov_map, self.player.x, self.player.y, self.player.fov_radius, self.player.light_walls,
                      self.fov_algorithm)

        self.game_state = GameStates.PLAYERS_TURN

    def game_turn(self, player_action):
        if self.game_state == GameStates.PLAYERS_TURN:
            self.player_turn(player_action)
        elif self.game_state == GameStates.ENEMY_TURN:
            self.enemy_turn()

        # Si une action a devoilé de nouvelles tiles, on les considère comme discovered.
        # TODO: Aujourd'hui le recompute du fov se fait dans le render et ailleurs. A reunir.
        if self.fov_recompute:
            discover_new_tiles(self.map)

    def enemy_turn(self):
        for entity in self.map.entities:
            if entity != self.player:
                print('The ' + entity.name + ' ponders the meaning of its existence.')
        self.enemy_end_turn()

    def enemy_end_turn(self):
        self.game_state = GameStates.PLAYERS_TURN

    def player_turn(self, player_action):
        # on recupere les actions faites par le joueur pour les gerer.
        move = player_action.get('move')

        if move:
            dx, dy = move
            # on verifie que l on peut deplacer le personnage.  # TODO: On le garde ici?
            destination_x = self.player.x + dx
            destination_y = self.player.y + dy

            # s il n y a pas de tuile bloquante...
            if not self.map.is_blocked(destination_x, destination_y):
                # y a t il des entités bloquantes?
                target = get_blocking_entities_at_location(self.map.entities, destination_x, destination_y)
                if target:
                    print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                else:
                    self.player.move(dx, dy)
                    self.fov_recompute = True
                    # fin du tour. # TODO : Meilleur moyen pour dire que le tour est fini.
                    self.player_end_turn()

    def player_end_turn(self):
        self.game_state = GameStates.ENEMY_TURN





