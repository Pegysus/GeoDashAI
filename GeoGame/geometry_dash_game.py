from GeoGame.utilities import settings
from GeoGame.geolevel import Level
import sys
import pygame
from pygame.locals import *

# import from specific level settings
GAME_WIDTH = settings.screen_width
GAME_HEIGHT = settings.screen_height

on_ground = False
game_over = False


def run_game():
    """main game loop"""
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    clock = pygame.time.Clock()
    level = Level(settings.level, screen, (GAME_WIDTH, GAME_HEIGHT))
    global on_ground, game_over

    # main game loop
    running = True
    while running:
        if level.game_over:
            return True

        for event in pygame.event.get():
            # game will officially "end" once the window closes
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                level.player_jump()
        # background color
        screen.fill('black')

        level.run()
        pygame.display.update()
        on_ground = level.on_ground
        # set frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    while True:
        if not run_game():
            break
