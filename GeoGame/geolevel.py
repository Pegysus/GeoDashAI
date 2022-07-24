import pygame
from GeoGame.tiletypes.block import Block
from GeoGame.tiletypes.spike_up import SpikeUp
from GeoGame.tiletypes.end import End
from GeoGame.tiletypes.player import Player
from GeoGame.utilities.settings import tile_size


class Level:
    SHIFT_SPEED = 7
    GAME_OVER = 0

    def __init__(self, data, surface, dimen):
        self._display = surface
        self._blocks = pygame.sprite.Group()
        self._spikes = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()
        self._width, self._height = dimen
        self.setup(data)
        self._world_shift = Level.SHIFT_SPEED

        self.distance = 0

    def setup(self, layout):
        for rows, r in enumerate(layout):
            for cols, cell in enumerate(r):
                if cell == 'X':
                    self._blocks.add(Block((cols * tile_size, rows * tile_size), tile_size))
                elif cell == '|':
                    self._blocks.add(End((cols * tile_size, rows * tile_size), tile_size))
                elif cell == 'S':
                    self._player.add(Player((cols * tile_size, rows * tile_size), tile_size))
                elif cell == 'U':
                    self._spikes.add(SpikeUp((cols * tile_size, rows * tile_size), (tile_size, tile_size)))

    def _horz_mvt_collision(self):
        cube = self._player.sprite
        cube.rect.x += cube.x_speed

        for block in self._blocks.sprites():
            if cube and block.rect.colliderect(cube.collideRect):
                self.stop()

        for spike in self._spikes.sprites():
            if cube and spike.collideRect.colliderect(cube.collideRect):
                self.stop()

    def _vert_mvt_collision(self):
        cube = self._player.sprite

        if cube and cube.midair:
            cube.apply_gravity()
            if cube.midair_ticks > 5:
                cube.rotate()
        elif cube:
            cube.reset_angle()
            cube.direction.y = 0
            cube.midair_ticks = 0

        if cube and not any(block.rect.colliderect(cube.collideRect) for block in self._blocks.sprites()):
            cube.midair = True
            cube.midair_ticks += 1

        for block in self._blocks.sprites():
            if cube and block.rect.colliderect(cube.collideRect):
                if cube.direction.y > 0:
                    cube.rect.bottom = block.rect.top
                    cube.collideRect.bottom = block.rect.top
                    cube.direction.y = 0
                    cube.midair = False

                elif cube.direction.y < 0:
                    cube.rect.top = block.rect.bottom
                    cube.collideRect.top = block.rect.bottom
                    cube.direction.y = 0

        for spike in self._spikes.sprites():
            if cube and spike.collideRect.colliderect(cube.collideRect):
                self.stop()

    def run(self):
        self._blocks.update(self._world_shift)
        self._blocks.draw(self._display)
        self._spikes.update(self._world_shift)
        self._spikes.draw(self._display)

        if self._player.sprite:
            self._player.update()

            self._horz_mvt_collision()
            self._vert_mvt_collision()
            self._player.draw(self._display)

        if any(type(b) is End and b.rect.right <= self._width for b in self._blocks):
            self._world_shift = 0
        if self._world_shift == 0 and self._player.sprite:
            self._player.sprite.x_speed = Level.SHIFT_SPEED

        self.distance += self._world_shift/32

    def stop(self):
        cube = self._player.sprite
        if cube:
            cube.kill()
        self._world_shift = Level.GAME_OVER
        # for display purposes
        print(self.distance)
