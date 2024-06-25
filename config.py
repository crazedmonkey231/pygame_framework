import os
import pygame
from pygame import display, Surface, Clock, Vector2
from pygame.font import Font
from pygame.mixer import Sound
from pygame.sprite import Sprite, RenderUpdates, LayeredUpdates
from game import Game
from game_object import (GameObject, GameObjectBase, GameObjectWithComponents, Character, Player, AiPlayer, Effect,
                         Widget)
from game_object_component import (GameObjectComponent, HealthComponent, PowerTrackerComponent, CountDownComponent,
                                   MovementComponent)


def map_range(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


game: Game = Game()
