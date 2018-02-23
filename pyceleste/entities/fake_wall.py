from PIL import Image

from .entity import Entity
from .entity import register_entity


@register_entity('fakeWall')
class FakeWall(Entity):

    render_mode = 'hide'

    def __init__(self, element, level):
        super().__init__(element, level)
        self.id = int(element.get('id'))
        self.tiletype = element.get('tiletype')
        self.width = int(element.get('width'))
        self.height = int(element.get('height'))
        self.x = int(element.get('x'))
        self.y = int(element.get('y'))
        self.originX = int(element.get('originX'))
        self.originY = int(element.get('originY'))
        self.play_transition = element.get('playTransitionReveal') == 'True'

    def render(self, im, x=0, y=0):
        if self.render_mode == 'hide':
            pass
        elif self.render_mode == 'fill':
            self.render_fill(im, x=x, y=y)
        else:
            raise ValueError('Unexpected render mode: {}'
                             .format(self.render_mode))

    def render_fill(self, im, x=0, y=0):
        tile_box = (self.y // 8,
                    self.x // 8,
                    (self.y + self.height) // 8,
                    (self.x + self.width) // 8)
        overlay = Image.new('RGBA', (self.width, self.height))
        shadow_map = self.level.solids.shadow(tile_box, self.tiletype)
        shadow_map.render(overlay, x=0, y=0, window=tile_box)
        im.alpha_composite(overlay, dest=(max(self.x, 0), max(self.y, 0)))
