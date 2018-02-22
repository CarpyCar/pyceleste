import pathlib


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
        pass
