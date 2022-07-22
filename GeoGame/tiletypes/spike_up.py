import pygame


class SpikeUp(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(topleft=pos)

        pygame.draw.polygon(self.image, '#9e9e9e', [(0, 32), (16, 0), (32, 32)])

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x_speed):
        self.rect.x += -x_speed
