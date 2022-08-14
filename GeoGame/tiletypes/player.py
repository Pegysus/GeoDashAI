import pygame


# player subclass
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # create surface to draw on (pygame.SRCALPHA to allow rotations outside of the surface)
        self.default_cube = pygame.Surface((size, size), pygame.SRCALPHA)
        self.default_cube.fill('red')
        self.image = self.default_cube

        # first rect is for the cube including while it is spinning, second rect is for the collision detections
        # (stays still as rotation animation occurs)
        self.rect = self.image.get_rect(topleft=pos)
        self.collideRect = pygame.rect.Rect((0, 0), (size, size))
        self.collideRect.center = self.rect.center

        # jumping mechanic variables
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.x_speed = 0
        self.angle = 0
        self.jump_speed = -10.5

        self.midair = False
        self.midair_ticks = 0
        self.jumping = False

    # binds jump to spacebar for gameplay
    def get_input(self):
        """inputs from keyboard/mouse of player"""
        keys = pygame.key.get_pressed()

        # if keys[pygame.K_SPACE] and not self.midair:
        #     self.jump()

    def apply_gravity(self):
        """gravity mechanics of the game"""
        self.direction.y += self.gravity

        # shift direction of both the cube and the collision rect of the cube
        self.rect.y += self.direction.y
        self.collideRect.y += self.direction.y

    def jump(self):
        """makes cube jump"""
        self.direction.y = self.jump_speed
        self.midair = True
        self.jumping = True

    def rotate(self):
        """rotation animation while midair"""
        self.image = pygame.transform.rotate(self.default_cube, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle = (self.angle - 8) % 360

    def reset_angle(self):
        """becomes flat once on the floor again"""
        self.angle = 0
        self.image = pygame.transform.rotate(self.default_cube, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """moves the cube as game goes on"""
        self.get_input()
        # makes sure the collision cube is in the center of the cube after any movements
        self.collideRect.center = self.rect.center

    def die(self):
        """if hit, get rid of cube"""
        self.kill()
