from .entity import Entity
from .entity import register_entity


@register_entity('jumpThru')
class JumpThru(Entity):

    def __init__(self, element):
        super().__init__(element)
        self.id = int(element.get('id'))
        self.typ = element.get('type', 'default')
        self.x = int(element.get('x'))
        self.y = int(element.get('y'))
        self.originX = int(element.get('originX'))
        self.originY = int(element.get('originY'))
        self.size = int(element.get('width'))

    def bitmap_path(self):
        bitmaps_dir = self.atlas_dir / 'objects' / 'jumpthru'
        typ = 'wood' if self.typ == 'default' else self.typ
        return bitmaps_dir / typ

    def render(self, im, x=0, y=0):
        bitmap, meta_info = self.load_bitmap()
        dest_x = x + self.x + meta_info['X']
        dest_y = y + self.y + meta_info['Y']
        width = meta_info['Width'] // 3
        count = self.size // width
        # draw left edge
        im.alpha_composite(bitmap, dest=(dest_x, dest_y),
                           source=(0, 0, 8, 8))
        dest_x += width
        for _ in range(1, count - 1):
            im.alpha_composite(bitmap, dest=(dest_x, dest_y),
                               source=(8, 0, 16, 8))
            dest_x += width
        im.alpha_composite(bitmap, dest=(dest_x, dest_y),
                           source=(16, 0, 24, 8))
        
