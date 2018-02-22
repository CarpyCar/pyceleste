from .entity import Entity
from .entity import register_entity


@register_entity('crumbleBlock')
class CrumbleBlock(Entity):

    def __init__(self, element, level):
        super().__init__(element, level)
        self.id = int(element.get('id'))
        self.texture = element.get('texture', 'default')
        self.width = int(element.get('width'))
        self.x = int(element.get('x'))
        self.y = int(element.get('y'))
        self.originX = int(element.get('originX'))
        self.originY = int(element.get('originY'))

    def bitmap_path(self):
        bitmaps_dir = self.atlas_dir / 'objects' / 'crumbleBlock'
        return bitmaps_dir / self.texture

    def render(self, im, x=0, y=0):
        bitmap, _ = self.load_bitmap()
        dest_x = x + self.x
        dest_y = y + self.y
        boxes = [(i * 8, 0, (i + 1) * 8, 8) for i in range(4)]
        count = self.width // 8
        for i in range(count):
            box = boxes[i % len(boxes)]
            im.alpha_composite(bitmap, dest=(dest_x + (i * 8), dest_y),
                               source=box)
