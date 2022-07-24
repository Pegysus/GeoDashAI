import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.default_cube = pygame.Surface((size, size), pygame.SRCALPHA)
        self.default_cube.fill('red')
        self.image = self.default_cube

        self.rect = self.image.get_rect(topleft=pos)
        self.collideRect = pygame.rect.Rect((0, 0), (size, size))
        self.collideRect.center = self.rect.center

        # jumping mechanic
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.x_speed = 0
        self.angle = 0
        self.jump_speed = -10.5

        self.midair = False
        self.midair_ticks = 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.midair:
            self.jump()

        if keys[pygame.K_0]:
            self.reset_angle()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.collideRect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.midair = True

    def rotate(self):
        self.image = pygame.transform.rotate(self.default_cube, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle = (self.angle - 6.7) % 360

    def reset_angle(self):
        self.angle = 0
        self.image = pygame.transform.rotate(self.default_cube, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.get_input()
        self.collideRect.center = self.rect.center

    def die(self):
        self.kill()
