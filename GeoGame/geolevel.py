import pygame
from GeoGame.tiletypes.block import Block
from GeoGame.tiletypes.end import End
from GeoGame.utilities.settings import tile_size


class Level:
    def __init__(self, data, surface, dimen):
        self._display = surface
        self._blocks = pygame.sprite.Group()
        self._width, self._height = dimen
        self.setup(data)
        self._world_shift = 4

    def setup(self, layout):
        for rows, r in enumerate(layout):
            for cols, cell in enumerate(r):
                if cell == 'X':
                    self._blocks.add(Block((cols * tile_size, rows * tile_size), tile_size))
                elif cell == '|':
                    self._blocks.add(End((cols * tile_size, rows * tile_size), tile_size))

    def run(self):
        self._blocks.update(self._world_shift)
        if any(type(b) is End and b.rect.right <= self._width for b in self._blocks):
            self._world_shift = 0

        self._blocks.draw(self._display)
