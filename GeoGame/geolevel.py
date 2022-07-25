import pygame
from GeoGame.tiletypes.block import Block
from GeoGame.tiletypes.spike_up import SpikeUp
from GeoGame.tiletypes.end import End
from GeoGame.tiletypes.player import Player
from GeoGame.utilities.settings import tile_size


class Level:
    # global variables
    SHIFT_SPEED = 7
    GAME_OVER = 0

    def __init__(self, data, surface, dimen):
        # block init
        self._display = surface
        self._blocks = pygame.sprite.Group()
        self._spikes = pygame.sprite.Group()
        self._end = pygame.sprite.Group()

        # player init
        self._player = pygame.sprite.GroupSingle()
        self._width, self._height = dimen
        self.setup(data)
        self._world_shift = Level.SHIFT_SPEED

        # win conditions + stats
        self.win = False
        self.distance = 0

    def setup(self, layout):
        """read settings and setup using the string of the level"""
        for rows, r in enumerate(layout):
            for cols, cell in enumerate(r):
                # if statement to check for types of blocks
                if cell == 'X':
                    self._blocks.add(Block((cols * tile_size, rows * tile_size), tile_size))
                elif cell == '|':
                    self._end.add(End((cols * tile_size, rows * tile_size), tile_size))
                elif cell == 'S':
                    self._player.add(Player((cols * tile_size, rows * tile_size), tile_size))
                elif cell == 'U':
                    self._spikes.add(SpikeUp((cols * tile_size, rows * tile_size), (tile_size, tile_size)))

    def _horz_mvt_collision(self):
        """checks for any horizontal collisions"""
        cube = self._player.sprite
        cube.rect.x += cube.x_speed

        # block collisions (horizontal = loss)
        for block in self._blocks.sprites():
            if cube and block.rect.colliderect(cube.collideRect):
                self.stop()

        # spike collisions
        for spike in self._spikes.sprites():
            if cube and spike.collideRect.colliderect(cube.collideRect):
                self.stop()

        # check for game to finish
        for e in self._end.sprites():
            if cube and e.rect.colliderect(cube.collideRect):
                self.finish_game()

    def _vert_mvt_collision(self):
        """checks for any vertical collisions"""
        cube = self._player.sprite

        # if cube is midair, apply gravity
        if cube and cube.midair:
            cube.apply_gravity()
            # cube will technically be "midair" for 1-2 ticks when on top of block, so prevent rotations
            # when cube is just moving to the right
            if cube.midair_ticks > 3:
                cube.rotate()
        elif cube:
            # makes sure cube is horizontal and going upwards
            cube.reset_angle()
            cube.direction.y = 0
            cube.midair_ticks = 0

        # checks if cube is midair
        if cube and not any(block.rect.colliderect(cube.collideRect) for block in self._blocks.sprites()):
            cube.midair = True
            cube.midair_ticks += 1

        # block collisions
        for block in self._blocks.sprites():
            if cube and block.rect.colliderect(cube.collideRect):
                # makes sure cube doesn't clip through any of the blocks
                if cube.direction.y > 0:
                    cube.rect.bottom = block.rect.top
                    cube.collideRect.bottom = block.rect.top
                    cube.direction.y = 0
                    cube.midair = False

                elif cube.direction.y < 0:
                    cube.rect.top = block.rect.bottom
                    cube.collideRect.top = block.rect.bottom
                    cube.direction.y = 0

        # spike collisions
        for spike in self._spikes.sprites():
            if cube and spike.collideRect.colliderect(cube.collideRect):
                self.stop()

    def run(self):
        """main running loop/function"""
        # update all the tiles/entities in the game
        self._blocks.update(self._world_shift)
        self._blocks.draw(self._display)
        self._end.update(self._world_shift)
        self._end.draw(self._display)
        self._spikes.update(self._world_shift)
        self._spikes.draw(self._display)

        # if sprite isn't killed yet
        if self._player.sprite:
            # update movement and check collisions
            self._player.update()

            self._horz_mvt_collision()
            self._vert_mvt_collision()
            self._player.draw(self._display)

        # if reached the end, stop shifting the whole world and shift only the cube
        if any(b.rect.right <= self._width for b in self._end):
            self._world_shift = 0
        if self._world_shift == 0 and self._player.sprite:
            self._player.sprite.x_speed = Level.SHIFT_SPEED

        self.distance += Level.SHIFT_SPEED/32

    def stop(self):
        """stops the cube/kills it once collided to an object"""
        cube = self._player.sprite
        if cube:
            cube.kill()
        self._world_shift = Level.GAME_OVER
        # for display purposes
        print(self.distance)

    def finish_game(self):
        """level is completed"""
        self.win = True
        print('You Win!')
        self.stop()
