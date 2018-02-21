import struct


class Reader(object):

    def __init__(self, path):
        self.file = open(path, 'rb')
        self._values = {
            0: self.bool,
            1: self.uint8,
            2: self.int16,
            3: self.int32,
            4: self.float32,
            5: self.entry,
            6: self.str,
            7: self.run_length
            }

    def bool(self):
        return bool(self.uint8())

    def uint8(self):
        return ord(self.file.read(1))

    def int16(self):
        return struct.unpack('<h', self.file.read(2))[0]

    def uint16(self):
        return struct.unpack('<H', self.file.read(2))[0]

    def int32(self):
        return struct.unpack('<i', self.file.read(4))[0]

    def float32(self):
        return struct.unpack('<f', self.file.read(4))[0]

    def varnum(self):
        """Read a variable length integer.
        
        The integers are little-endian, with the high-order bit indicating
        whether or not there are additional bytes and the remaining 7 bits
        comprising the value of the integer.
        """
        result = 0
        count = 0
        while True:
            val = self.uint8()
            result += (val & 0x7f) << (count * 7)
            if val & 0x80 == 0:
                return result
            count += 1

    def str(self):
        length = self.varnum()
        return self.file.read(length).decode('ascii')

    def run_length(self):
        len = self.uint16()
        result = []
        for _ in range(len // 2):
            count = self.uint8()
            value = self.uint8()
            result.extend([chr(value)] * count)
        return ''.join(result)

    def dict(self):
        result = {}
        name = result['name'] = self.entry()
        attributes = {}
        num_attributes = self.uint8()
        for _ in range(num_attributes):
            attr_name = self.entry()
            attr_value = self.value()
            if attr_name in attributes:
                raise ValueError('Duplicate key {}'.format(attr_name))
            attributes[attr_name] = attr_value
        result['attributes'] = attributes
        num_children = self.uint16()
        children = {}
        for _ in range(num_children):
            child_name, child = self.dict()
            if child_name not in children:
                children[child_name] = []
            children[child_name].append(child)
        result['children'] = children
        return name, result

    def entry(self):
        key = self.uint16()
        return self.entries[key]

    def value(self):
        """Read an encoded value.

        The first byte indicates the type, then we dispatch to the appropriate
        method to read the value itself.
        """
        type_id = self.uint8()
        return self._values[type_id]()
