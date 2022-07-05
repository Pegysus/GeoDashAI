import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('#54575c')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_speed):
        self.rect.x += -x_speed
