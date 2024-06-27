import os
import pygame
from pygame import display, Surface, Clock, Vector2, Rect
from pygame.font import Font
from pygame.mixer import Sound
from pygame.sprite import Sprite, RenderUpdates, LayeredUpdates
from game import Game
from game_component import GameComponent
from game_object import (GameObject, GameObjectBase, GameObjectWithComponents, Character, Player, AiPlayer, Effect,
                         Widget, NoneSound)
from game_object_component import (GameObjectComponent, HealthComponent, PowerTrackerComponent, CountDownComponent,
                                   MovementComponent, GameObjectHolder)

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# Mixer enabled
mixer_initialized = pygame.mixer or pygame.mixer.get_init()

# Health max config, for damage and health component
config_health_max: float = 999999

# Render layers
render_layer_default: int = 0
render_layer_middle: int = 1
render_layer_top: int = 2


# Map a range to another
def map_range(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


# Image loader
def load_image(self, name, color_key=None, scale=1) -> tuple[Surface, Rect]:
    image = pygame.image.load(os.path.join(data_dir, name)).convert_alpha()
    size = image.get_size()
    image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)
    return image, image.get_rect()


# Sound loader
def load_sound(self, name) -> object:
    if not mixer_initialized:
        return NoneSound()
    return pygame.mixer.Sound(os.path.join(data_dir, name))


# Main game object
game: Game = Game()
