import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # jumping mechanic
        self.direction = pygame.math.Vector2(0,0)
        self.gravity = 0.8
        self.x_speed = 0
        self.jump_speed = -10.2
        self.midair = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.midair:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.midair = True

    def update(self):
        self.get_input()

    def die(self):
        self.kill()
