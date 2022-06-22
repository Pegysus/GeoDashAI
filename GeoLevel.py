import pygame

GAME_WIDTH = 1200
GAME_HEIGHT = 600

def main():
    pygame.init()
    screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('black')

        # Flip the display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
