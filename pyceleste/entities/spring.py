from .entity import Entity
from .entity import register_entity


@register_entity('spring')
class Spring(Entity):

    def __init__(self, element, level):
        super().__init__(element, level)
        self.id = int(element.get('id'))
        self.x = int(element.get('x'))
        self.y = int(element.get('y'))
        self.originX = int(element.get('originX'))
        self.originY = int(element.get('originY'))
        self.can_use = bool(element.get('playerCanUse'))

    def bitmap_path(self):
        return self.atlas_dir / 'objects' / 'spring' / '00'

    def render(self, im, x=0, y=0):
        bitmap, meta_info = self.load_bitmap()
        dest_x = x + self.x + meta_info['X'] - (meta_info['Width'] // 2)
        dest_y = y + self.y + meta_info['Y'] - meta_info['Height']
        im.alpha_composite(bitmap, dest=(dest_x, dest_y))
