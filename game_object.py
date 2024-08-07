from config import *
from game_object_components import HealthComponent, MovementComponent, CountDownComponent


#
# Game Object
#
class GameObject(Sprite):
    def __init__(self, parent=None):
        Sprite.__init__(self)
        from config import game
        self.game = game
        self.background_surface: Surface = None
        self.foreground_surface: Surface = None
        self.overlay_surface: Surface = None
        self.background_color = (0, 0, 0, 0)
        self.foreground_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0)
        self.parent: GameObject = parent if isinstance(parent, GameObject) else None
        self._layer: int = 0
        self.tags: set[str] = set()
        self.on_init()
        self.image = self.background_surface
        self.rect = self.image.get_rect() if self.image else None
        self.half_height = self.rect.height / 2 if self.rect else 0
        self.half_width = self.rect.width / 2 if self.rect else 0
        self.cached_center_vector2: Vector2 = Vector2(self.rect.center) if self.rect else Vector2(0, 0)

    def on_init(self):
        pass

    def update(self, *args, **kwargs):
        if self.background_surface:
            self.background_surface.fill(self.background_color)
            self.image.blit(self.background_surface, (0, 0))
        if self.foreground_surface:
            self.foreground_surface.fill(self.foreground_color)
            self.image.blit(self.foreground_surface, (0, 0))
        if self.overlay_surface:
            self.overlay_surface.fill(self.overlay_color)
            self.image.blit(self.overlay_surface, (0, 0))
        self.cached_center_vector2 = Vector2(self.rect.center) if self.rect else Vector2(0, 0)

    def on_destroy(self):
        pass

    def kill(self):
        self.on_destroy()
        self.game = None
        self.parent = None
        super().kill()

    def apply_damage(self, causer: Sprite = None, damage_amount: float = 0):
        pass

    def on_clicked(self):
        pass

    def on_un_clicked(self):
        pass

    def distance_to_game_object(self, other_sprite) -> float:
        if isinstance(other_sprite, GameObject):
            other_game_object: GameObject = other_sprite
            return Vector2(self.rect.center).distance_to(Vector2(other_game_object.rect.center))
        return -1

    def distance_to_position(self, target_pos: Vector2) -> float:
        return Vector2(self.rect.center).distance_to(target_pos)


#
# Game Object Base
#
class GameObjectBase(GameObject):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)


#
# Game Object With Components
#
class GameObjectWithComponents(GameObjectBase):
    def __init__(self, parent: GameObject = None):
        self._components: list[GameObjectComponent] = list()
        super().__init__(parent)

    def get_components(self):
        return self._components

    def on_init(self):
        super().on_init()
        activate_components(self._components)

    def on_destroy(self):
        super().on_destroy()
        deactivate_components(self._components)
        destroy_components(self._components)
        self._components.clear()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        update_components(self._components)

    def reset(self):
        reset_components(self._components)

    def add_game_object_component(self, component):
        from game_object_components import GameObjectComponent
        add_component(GameObjectComponent, self._components, component, self)

    def remove_game_object_component(self, component, optional_tags: set[str] = None):
        from game_object_components import GameObjectComponent
        remove_component(GameObjectComponent, self._components, component, optional_tags)

    def apply_damage(self, causer: Sprite = None, damage_amount: float = 0):
        super().apply_damage(causer, damage_amount)
        health_component: HealthComponent = get_component_by_class(self._components, HealthComponent)
        if health_component:
            health_component.update_health(damage_amount)


# ----------------------------------------------------------------------------------------------------------------------

#
# Game Object With Movement
#
class GameObjectWithMovement(GameObjectWithComponents):
    def __init__(self, parent: GameObject = None, move_speed: Vector2 = Vector2(0, 0)):
        super().__init__(parent)
        self._components.append(MovementComponent(self, move_speed))


#
# Game Object With Health
#
class GameObjectWithHealth(GameObjectWithComponents):
    def __init__(self, parent: GameObject = None, health: float = 100, health_max: float = 100,
                 health_update_change: float = 0):
        super().__init__(parent)
        self._components.append(HealthComponent(self, health, health_max, health_update_change))


#
# Game Object With Timer
#
class GameObjectWithTimer(GameObjectWithComponents):
    def __init__(self, parent: GameObject = None, time_to_live: float = 0):
        super().__init__(parent)
        self._components.append(CountDownComponent(self, time_to_live))


#
# Grid Slot Game Object
#
class GridSlotGameObject(GameObjectWithComponents):
    def __init__(self, size: Vector2):
        self.size: Vector2 = size
        super().__init__(None)

    def on_init(self):
        super().on_init()
        self._layer = -1
        self.background_surface = Surface((self.size.x, self.size.y)).convert_alpha()
        self.foreground_surface = Surface((self.size.x, self.size.y)).convert_alpha()
        self.overlay_surface = Surface((self.size.x, self.size.y)).convert_alpha()
        self.background_color = (255, 255, 255, 255)
        self.foreground_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0)


#
# Light Grid Slot Game Object
#
class LightGridSlotGameObject(GridSlotGameObject):
    def __init__(self, size: Vector2):
        super().__init__(size)

    def on_init(self):
        super().on_init()
        self._layer = 1
        self.background_surface = Surface((self.size.x, self.size.y)).convert_alpha()
        self.foreground_surface = Surface((self.size.x, self.size.y)).convert_alpha()
        self.overlay_surface = Surface((self.size.x, self.size.y)).convert_alpha()
        self.background_color = (0, 0, 0, 0)
        self.foreground_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0)


# ----------------------------------------------------------------------------------------------------------------------


#
# Character
#
class Character(GameObjectWithMovement):
    def __init__(self, parent: GameObject = None):
        self.is_player_controlled: bool = False
        super().__init__(parent)
        self._components.append(HealthComponent(self))


#
# Player
#
class Player(Character):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.is_player_controlled: bool = True

    def on_init(self):
        super().on_init()
        self.background_surface = Surface((1, 1)).convert_alpha()
        self.background_color = (0, 0, 0, 0)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.rect.center = pygame.mouse.get_pos()


#
# AiPlayer
#
class AiPlayer(Character):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)


# ----------------------------------------------------------------------------------------------------------------------

#
# Projectile
#
class Projectile(GameObjectWithMovement):
    def __init__(self, parent, move_speed: Vector2):
        super().__init__(parent, move_speed)
        self._components.append(HealthComponent(self))


# ----------------------------------------------------------------------------------------------------------------------

#
# Effect
#
class Effect(GameObjectWithMovement):
    def __init__(self, parent: GameObject = None, move_speed: Vector2 = Vector2(0, 0)):
        super().__init__(parent, move_speed)


#
# Effect With Timer
#
class EffectWithTimer(Effect):
    def __init__(self, parent: GameObject = None, move_speed: Vector2 = Vector2(0, 0), time_to_live: float = 0):
        super().__init__(parent, move_speed)
        self._components.append(CountDownComponent(self, time_to_live))


# ----------------------------------------------------------------------------------------------------------------------

#
# Widget
#
class Widget(GameObjectWithComponents):
    def __init__(self, parent: GameObject = None, dimension: Vector2 = Vector2(5, 5)):
        super().__init__(parent)
        self.widget_dimension: Vector2 = dimension
        self.widget_width = dimension.x
        self.widget_height = dimension.x
        self.widget_half_height = self.widget_height / 2
        self.widget_half_width = self.widget_width / 2


#
# Widget With Movement
#
class WidgetWithMovement(Widget):
    def __init__(self, parent: GameObject = None, dimension: Vector2 = Vector2(5, 5),
                 move_speed: Vector2 = Vector2(0, 0)):
        super().__init__(parent, dimension)
        self._components.append(MovementComponent(self, move_speed))


#
# Widget With Timer
#
class WidgetWithTimer(Widget):
    def __init__(self, parent: GameObject = None, time_to_live: float = 0):
        super().__init__(parent)
        self._components.append(CountDownComponent(self, time_to_live))


#
# Progress Bar
#
class ProgressBar(Widget):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.percent_fill: float = 0.0

    def update(self, *args, **kwargs):
        pass
