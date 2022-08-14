import pygame.constants as pc
import GeoGame.geometry_dash_game as geogame
from players.pygame_player import PyGamePlayer
from learner.qlearn import QLearning

ACTIONS = [pc.K_SPACE, pc.K_UNKNOWN]


class GeoDashPlayer(PyGamePlayer):
    def __init__(self, force_game_fps=10, run_real_time=True):
        super().__init__(force_game_fps=force_game_fps, run_real_time=run_real_time)
        self.dql = QLearning(ACTIONS, save=True)

    def get_keys_pressed(self, screen_array, feedback, terminal):
        return self.dql.step(screen_array, feedback, terminal) if geogame.on_ground else [pc.K_UNKNOWN]

    def get_feedback(self):
        reward = -1000.0 if geogame.game_over else 1.0
        return reward, geogame.game_over

    def start(self):
        super().start()
        geogame.main()
