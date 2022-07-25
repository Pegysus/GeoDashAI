from GeoGame.utilities import settings
from GeoGame.geolevel import Level
import sys
import pygame

# import from specific level settings
GAME_WIDTH = settings.screen_width
GAME_HEIGHT = settings.screen_height


def main():
    """main game loop"""
    pygame.init()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    clock = pygame.time.Clock()
    level = Level(settings.level, screen, (GAME_WIDTH, GAME_HEIGHT))

    # main game loop
    running = True
    while running:
        for event in pygame.event.get():
            # game will officially "end" once the window closes
            if event.type == pygame.QUIT:
                running = False
        # background color
        screen.fill('black')

        level.run()
        pygame.display.update()
        # set frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
