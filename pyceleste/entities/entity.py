import pathlib

import yaml
from PIL import Image


entities = {}


def register_entity(*names):
    def decorator(fn):
        for name in names:
            entities[name] = fn
        return fn
    return decorator


def create_entity(element):
    if element.tag in entities:
        entity_type = entities[element.tag]
    else:
        entity_type = Entity
    return entity_type(element)


class Entity(object):

    atlas_dir = pathlib.Path('Graphics/Atlases/Gameplay')

    def __init__(self, element):
        self.element = element
        self.tag = element.tag

    def render(self, im, x=0, y=0):
        print('Unimplemented entity:', self.tag)

    def bitmap_path(self):
        """Return a pathlib.Path object representing the prefix of a bitmap."""
        raise NotImplementedError

    def load_bitmap(self):
        path = self.bitmap_path()
        bitmap = Image.open(path.with_suffix('.png'))
        meta_path = path.with_suffix('.meta.yaml')
        if meta_path.exists():
            with open(meta_path, 'r') as f:
                meta_info = yaml.load(f)
        else:
            meta_info = None
        return bitmap, meta_info
