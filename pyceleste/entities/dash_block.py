import numpy as np
from PIL import Image

from ..maps.tile_map import TileMap
from ..tiles import fg_tiles
from ..util.draw import border
from .entity import Entity
from .entity import register_entity


@register_entity('dashBlock')
class DashBlock(Entity):

    def __init__(self, element, level):
        super().__init__(element, level)
        self.id = int(element.get('id'))
        self.tiletype = element.get('tiletype')
        self.width = int(element.get('width'))
        self.height = int(element.get('height'))
        self.x = int(element.get('x'))
        self.y = int(element.get('y'))
        self.originX = int(element.get('originX'))
        self.originY = int(element.get('originY'))
        self.permanent = element.get('permanent') == 'True'
        self.blendin = element.get('blendin') == 'True'
        self.can_dash = element.get('canDash') == 'True'

    def render(self, im, x=0, y=0):
        if self.blendin:
            self.render_blendin(im, x=x, y=y)
        else:
            self.render_separate(im, x=x, y=y)

    def render_blendin(self, im, x=0, y=0):
        tile_box = (self.y // 8,
                    self.x // 8,
                    (self.y + self.height) // 8,
                    (self.x + self.width) // 8)
        overlay = Image.new('RGBA', (self.width, self.height))
        shadow_map = self.level.solids.shadow(tile_box, self.tiletype)
        shadow_map.render(overlay, x=0, y=0, window=tile_box)
        border(overlay)
        im.alpha_composite(overlay, dest=(max(self.x, 0), max(self.y, 0)))

    def render_separate(self, im, x=0, y=0):
        tile_width = self.width // 8
        tile_height = self.height // 8
        array = np.empty((tile_height, tile_width), dtype=np.unicode_)
        array[...] = self.tiletype
        tile_map = TileMap.from_array(array, fg_tiles, tile_width, tile_height,
                                      extend=False)
        overlay = Image.new('RGBA', (self.width, self.height))
        tile_map.render(overlay, x=0, y=0)
        border(overlay)
        im.alpha_composite(overlay, dest=(max(self.x, 0), max(self.y, 0)))
