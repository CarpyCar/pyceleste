from ..io.reader import Reader


class MapReader(Reader):

    def decode(self):
        if self.str() != 'CELESTE MAP':
            raise ValueError('Invalid celeste map (invalid header)')
        package = self.str()
        num_entries = self.int16()
        self.entries = [self.str() for _ in range(num_entries)]
        return self.dict()[1]
