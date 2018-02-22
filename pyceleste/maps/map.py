from PIL import ImageDraw
from PIL import ImageFont

from .tile_map import TileMap
from ..tiles import fg_tiles
from ..tiles import bg_tiles


class Map(object):

    def __init__(self, etree):
        self.etree = etree
        self.levels = []
        for level in self.etree.find('levels').findall('level'):
            self.levels.append(Level(level))


class Level(object):

    def __init__(self, etree):
        self.etree = etree
        self.name = self.etree.get('name')
        self.width = int(self.etree.get('width'))
        self.height = int(self.etree.get('height'))
        self.solids = TileMap(self.etree.find('solids').text, fg_tiles, self.width // 8, self.height // 8)
        bg_str = self.etree.find('bg').text
        if bg_str is not None:
            self.bg = TileMap(bg_str, bg_tiles, self.width // 8, self.height // 8)
        else:
            self.bg = None

    def __repr__(self):
        return '<Level name={}>'.format(self.name)

    def render(self, im, x=0, y=0, draw_name=False):
        if self.bg is not None:
            self.bg.render(im, x=x, y=y)
        self.solids.render(im, x=x, y=y)
        if draw_name:
            font = ImageFont.truetype('resources/munro/Munro.ttf', 10)
            draw = ImageDraw.Draw(im)
            draw.text((2, 2), self.name[4:], font=font)
