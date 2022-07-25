import pygame


# "end" of level, a column of blocks specifying the end of the game
class End(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_speed):
        """update position of end tile as game moves"""
        self.rect.x += -x_speed
