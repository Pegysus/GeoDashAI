import pygame


# spike that faces upwards
class SpikeUp(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(topleft=pos)

        # a smaller collision rectangle, so there isn't a collision with a spike on the edge of the rectangular
        # collision box when it doesn't seem to be on the spike
        self.collideRect = pygame.rect.Rect((0, 0), (23, 23))
        self.collideRect.midbottom = self.rect.midbottom

        # draws the triangular spike
        pygame.draw.polygon(self.image, '#9e9e9e', [(0, 32), (16, 0), (32, 32)])

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x_speed):
        """updates the spike to move as the game moves/shifts"""
        self.rect.x += -x_speed
        self.collideRect.x += -x_speed
