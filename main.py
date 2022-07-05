from GeoGame.utilities import settings
from GeoGame.geolevel import Level
import sys
import pygame

GAME_WIDTH = settings.screen_width
GAME_HEIGHT = settings.screen_height


def main():
    pygame.init()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    clock = pygame.time.Clock()
    level = Level(settings.level, screen, (GAME_WIDTH, GAME_HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        level.run()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
