import click
from PIL import Image

from pyceleste.maps.tile_map import TileMap
from pyceleste.maps.reader import MapReader
from pyceleste.tiles import TileCollection


@click.command()
@click.argument('mapfile', type=click.Path(exists=True))
@click.option('--level', '-l', default=0)
def main(mapfile, level):
    reader = MapReader(mapfile)
    map = reader.decode()
    level = map['children']['levels'][0]['children']['level'][level]
    w = level['attributes']['width'] // 8
    h = level['attributes']['height'] // 8
    fg_tiles = TileCollection('Content/Graphics/ForegroundTiles.xml')
    fg_str = level['children']['solids'][0]['attributes']['innerText']
    fg_map = TileMap(fg_str, fg_tiles, width=w, height=h)
    bg_tiles = TileCollection('Content/Graphics/BackgroundTiles.xml')
    bg_str = level['children']['bg'][0]['attributes']['innerText']
    bg_map = TileMap(bg_str, bg_tiles, width=w, height=h)
    im = Image.new('RGBA', (fg_map.width * 8, fg_map.height * 8))
    im.paste((0, 0, 0, 255), (0, 0, fg_map.width * 8, fg_map.height * 8))
    bg_map.render(im, bg_tiles)
    fg_map.render(im, fg_tiles)
    im.save('test.png')


if __name__ == '__main__':
    main()
