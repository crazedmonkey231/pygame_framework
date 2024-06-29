from config import *


# Map a range to another
def map_range(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


# Clamp value between range
def clamp_value(value, start, stop):
    return min(max(value, start), stop)


# Image loader
def load_image(name, color_key=None, scale=1) -> tuple[Surface, Rect]:
    image = pygame.image.load(os.path.join(data_dir, name)).convert_alpha()
    size = image.get_size()
    image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)
    return image, image.get_rect()


# Sound loader
def load_sound(name) -> object:
    if not mixer_initialized:
        return NoneSound()
    return pygame.mixer.Sound(os.path.join(data_dir, name))


def get_component_by_class(comp_list, comp_class):
    for component in comp_list:
        if component.__class__ == comp_class:
            return component
    return None
