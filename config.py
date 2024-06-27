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


mixer_initialized = pygame.mixer or pygame.mixer.get_init()


# Health max config, for damage and health component
config_health_max: float = 999999

# Render layers
render_layer_default: int = 0
render_layer_middle: int = 1
render_layer_top: int = 2


def map_range(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


game: Game = Game()
