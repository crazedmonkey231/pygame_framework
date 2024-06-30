import os
import pygame
from collections import defaultdict
from pygame import display, Surface, Clock, Vector2, Rect
from pygame.font import Font
from pygame.mixer import Sound
from pygame.sprite import Sprite, RenderUpdates, LayeredUpdates
from util import map_range, clamp_value, load_image, load_sound
from component import (add_component, remove_component, get_component_by_class, update_components, activate_components,
                       deactivate_components, draw_components, reset_components, destroy_components)
from game import Game
from component import Component, GameComponent
from game_object import GameObject, GameObjectBase, GameObjectWithComponents, GridSlotGameObject
from component import GameObjectComponent
from game_object_components import HealthComponent, MovementComponent, CountDownComponent
from level import Level
from component import LevelComponent
from level_components import GridLevelComponent, DiscoGridLevelComponent


pygame.init()

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
render_layer_bottom: int = 1
render_layer_middle: int = 2
render_layer_top: int = 3

game: Game = Game()

