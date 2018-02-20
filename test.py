import click

from pyceleste.maps.reader import MapReader

@click.command()
@click.argument('mapfile', type=click.Path(exists=True))
def main(mapfile):
    reader = MapReader(mapfile)
    map = reader.decode()
    print(map['children']['levels'][0]['children']['level'][0]['attributes'])
    print(map['children']['levels'][0]['children']['level'][0]['children'])
    #print(map['children']['levels'][0])


if __name__ == '__main__':
    main()
