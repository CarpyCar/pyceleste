import click
import lxml.etree as ElementTree
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from pyceleste.maps.reader import MapReader
from pyceleste.tiles import fg_tiles
from pyceleste.tiles import bg_tiles


@click.command()
@click.argument('path', type=click.Path(exists=True))
def main(path):
    fg_tiles.load('Content/Graphics/ForegroundTiles.xml')
    bg_tiles.load('Content/Graphics/BackgroundTiles.xml')
    reader = MapReader(path)
    map = reader.decode()
    for i, level in enumerate(map.levels):
        im = Image.new('RGBA', (level.width, level.height))
        im.paste((0, 0, 0, 255), (0, 0, level.width, level.height))
        level.render(im, draw_name=True)
        im.save('dump/{}.png'.format(level.name))


if __name__ == '__main__':
    main()
