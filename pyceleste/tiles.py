import pathlib
import lxml.etree as ElementTree

from PIL import Image


# TODO: probably shouldn't be hardcoded 8)
TILESET_DIR = pathlib.Path('Graphics/Atlases/Gameplay/tilesets')


class TileCollection(object):
    """Holds a series of Tilesets.
    
    This corresponds to one of the tile XML files packaged with the game (e.g.
    ForegroundTiles.xml).
    """

    def __init__(self):
        self.tilesets = {}

    def load(self, path):
        parser = ElementTree.XMLParser(remove_comments=True)
        self.tree = ElementTree.parse(path, parser=parser)
        for tileset in self.tree.getroot():
            if 'copy' in tileset.attrib:
                copy = self.tilesets[tileset.attrib['copy']]
            else:
                copy = None
            tileset = Tileset(tileset, copy=copy)
            self.tilesets[tileset.id] = tileset

    def __getitem__(self, id):
        return self.tilesets[id]


# Create singletons
fg_tiles = TileCollection()
bg_tiles = TileCollection()


class Tileset(object):

    TILE_SIZE = 8

    def __init__(self, tree, copy=None):
        if copy is not None:
            self.ignores = copy.ignores
            self.masks = dict(copy.masks)
            self.sprites = dict(copy.sprites)
            self.centers = list(copy.centers)
            self.paddings = list(copy.paddings)
            # TODO: if you just blindly copy the centers/paddings, then when
            # you update tiles there may be stale entries
        else:
            self.ignores = None
            self.masks = {}
            self.sprites = {}
            self.centers = []
            self.paddings = []
        self.id = tree.attrib['id']
        self.path = tree.attrib['path']
        self.bitmap = Image.open(TILESET_DIR / (self.path + '.png'))
        self.ignores = tree.attrib.get('ignores', None)
        if self.ignores is not None:
            self.ignores = self.ignores.split(',')
        for set in tree:
            mask = set.attrib['mask']
            sprites = set.attrib.get('sprites', None)
            for coord in set.attrib['tiles'].split(';'):
                x, y = coord.split(',')
                x, y = int(x), int(y)
                self.masks[x, y] = mask
                self.sprites[x, y] = sprites
                if mask == 'center':
                    self.centers.append((x, y))
                if mask == 'padding':
                    self.paddings.append((x, y))

    def get_box(self, coord):
        """Convert a tile coordinate to a pixel bounding box on the bitmap."""
        x, y = coord
        return (x * self.TILE_SIZE, y * self.TILE_SIZE,
                (x + 1) * self.TILE_SIZE, (y + 1) * self.TILE_SIZE)

    def __getitem__(self, adjacency):
        """Given an adjacency string, return the coordinates of all tiles that
        match.

        If no candidates are returned, a center or padding tile should be used.
        """
        candidates = []
        for coord, mask in self.masks.items():
            if mask == 'center' or mask == 'padding':
                continue
            for adjacency_flag, mask_flag in zip(adjacency, mask):
                if adjacency_flag == '-':
                    continue
                if mask_flag != 'x' and adjacency_flag != mask_flag:
                    break
            else:
                candidates.append(coord)
        # TODO: handle sprites
        return candidates
