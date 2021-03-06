import random

from .entity import Entity
from .entity import register_entity


@register_entity('spikesUp', 'spikesDown', 'spikesLeft', 'spikesRight')
class Spikes(Entity):

    def __init__(self, element, level):
        super().__init__(element, level)
        self.id = int(element.get('id'))
        self.direction = self.tag[6:].lower()
        self.spike_type = element.get('type', 'default')
        if self.vertical:
            self.size = int(element.get('width'))
        else:
            self.size = int(element.get('height'))
        self.x = int(element.get('x'))
        self.y = int(element.get('y'))
        self.originX = int(element.get('originX'))
        self.originY = int(element.get('originY'))

    @property
    def vertical(self):
        return self.direction == 'up' or self.direction == 'down'

    def bitmap_path(self):
        bitmaps_dir = self.atlas_dir / 'danger' / 'spikes'
        glob_str = '{}_{}*.png'.format(self.spike_type, self.direction)
        candidates = list(bitmaps_dir.glob(glob_str))
        return random.choice(candidates).with_suffix('')

    def render(self, im, x=0, y=0):
        bitmap, meta_info = self.load_bitmap()
        width = meta_info['Width']
        height = meta_info['Height']
        dest_x = x + self.x + meta_info['X']
        if self.direction == 'left':
            dest_x -= width
        dest_y = y + self.y + meta_info['Y']
        if self.direction == 'up':
            dest_y -= height
        count = self.size // (width if self.vertical else height)
        for _ in range(count):
            im.alpha_composite(bitmap, dest=(dest_x, dest_y))
            if self.vertical:
                dest_x += width
            else:
                dest_y += height
