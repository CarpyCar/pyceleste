from lxml import etree

from ..io.reader import Reader
from .map import Map


class MapReader(Reader):

    def decode(self):
        if self.str() != 'CELESTE MAP':
            raise ValueError('Invalid celeste map (invalid header)')
        package = self.str()
        num_entries = self.int16()
        self.entries = [self.str() for _ in range(num_entries)]
        return Map(etree.ElementTree(self.element()))
