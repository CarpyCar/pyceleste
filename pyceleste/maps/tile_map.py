import random

import numpy as np


class TileMap(object):
    """A grid of tiles.

    Most indexing here is done array-style, i.e. (row, column).
    """

    TILE_SIZE = 8

    def __init__(self, string, tiles, width, height):
        self.width = width
        self.height = height
        self.tiles = tiles
        self.map = np.empty((height, width), dtype=np.unicode_)
        self.map[...] = '0'
        self.fill_map(string)

    def fill_map(self, string):
        """Fill this tilemap based on a tile string."""
        row, col = 0, 0
        for char in string:
            if char == '\n':
                for col in range(col, self.width):
                    self.map[row, col] = '0'
                row += 1
                col = 0
            else:
                self.map[row, col] = char
                col += 1

    def __getitem__(self, coord):
        """Index into this tilemap.

        If an out-of-bounds index is provided, edge-extend the tilemap.
        """
        row, col = coord
        if row < 0:
            row = 0
        elif row >= self.height:
            row = self.height - 1
        if col < 0:
            col = 0
        elif col >= self.width:
            col = self.width - 1
        return self.map[row, col]

    def check_padding(self, row, col):
        """Return True if this location qualifies as a padding cell.

        When a tile is surrounded, it is rendered as a padding cell if one of
        the cells two spaces away in the cardinal directions is empty.
        """
        return (self[row - 2, col] == '0' or self[row + 2, col] == '0'
                or self[row, col - 2] == '0' or self[row, col + 2] == '0')

    def padding_or_center(self, row, col, tileset):
        if self.check_padding(row, col):
            return tileset.paddings
        else:
            return tileset.centers

    def adjacency(self, center_row, center_col, ignore=None):
        """Return a string indicating this cell's adjacency.

        Adjacency strings are of the form XXX-XXX-XXX, representing a 3x3
        matrix in row-major order. A cell is 0 if that cell is either empty or
        occupied by an ignored tile, and 1 otherwise.
        """
        if ignore is None:
            ignore = []
        elif '*' in ignore:
            ignore = list(self.tiles.tilesets.keys())
            ignore.remove(self[center_row, center_col])
        if '0' not in ignore:
            ignore.append('0')

        row_strs = []
        for row in range(center_row - 1, center_row + 2):
            parts = []
            for col in range(center_col - 1, center_col + 2):
                parts.append('0' if self[row, col] in ignore else '1')
            row_strs.append(''.join(parts))
        adj = '-'.join(row_strs)
        return adj

    def render(self, image, x=0, y=0):
        """Render this TileMap onto a PIL Image at (x, y)."""
        for row in range(self.height):
            for col in range(self.width):
                if self[row, col] == '0':
                    continue
                tileset = self.tiles[self[row, col]]
                adjacency = self.adjacency(row, col, ignore=tileset.ignores)
                candidates = tileset[adjacency]
                if not candidates:
                    candidates = self.padding_or_center(row, col, tileset)
                tile_box = tileset.get_box(random.choice(candidates))
                dest = (col * self.TILE_SIZE, row * self.TILE_SIZE)
                image.alpha_composite(tileset.bitmap,
                                      dest=dest,
                                      source=tile_box)
