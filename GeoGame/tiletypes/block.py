import pygame


# subclass of sprite, draws a block that the player can stand on
class Block(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('#54575c')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_speed):
        """updates position of block tile as game moves/shifts"""
        self.rect.x += -x_speed
