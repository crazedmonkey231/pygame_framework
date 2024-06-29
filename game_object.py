from config import *


#
# Game Object
#
class GameObject(Sprite):
    def __init__(self, parent=None):
        Sprite.__init__(self)
        self.on_init()
        self.parent: GameObject = parent if isinstance(parent, GameObject) else None
        self._layer: int = render_layer_default
        self.tags: set[str] = set()
        self.half_height = self.rect.height / 2 if self.rect else 0
        self.half_width = self.rect.width / 2 if self.rect else 0
        self.background_surface: Surface = None
        self.background_color = (0, 0, 0, 0)
        self.foreground_surface: Surface = None
        self.foreground_color = (0, 0, 0, 0)
        self.overlay_surface: Surface = None
        self.overlay_color = (0, 0, 0, 0)

    def on_init(self):
        pass

    def on_destroy(self):
        pass

    def kill(self):
        self.on_destroy()
        self.parent = None
        super().kill()

    def apply_damage(self, causer: Sprite = None, damage_amount: float = 0):
        pass

    def on_clicked(self):
        pass

    def on_un_clicked(self):
        pass

    def distance_to_game_object(self, other_sprite) -> float:
        if issubclass(other_sprite, GameObject):
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
    def __init__(self, parent: GameObject = None, components: list = None):
        super().__init__(parent)
        if components is None:
            self._components: list[GameObjectComponent] = list()
        else:
            self._components = components
            if not all(issubclass(type(obj), GameObjectComponent) for obj in components):
                self._components: list[GameObjectComponent] = list(
                    [c for c in self._components if isinstance(c, GameObjectComponent)])
            activate_components(self._components)

    def on_destroy(self):
        super().on_destroy()
        deactivate_components(self._components)
        destroy_components(self._components)
        self._components.clear()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        update_components(self._components)

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


# ----------------------------------------------------------------------------------------------------------------------

#
# Character
#
class Character(GameObjectWithMovement):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.is_player_controlled: bool = False
        self._components.append(HealthComponent(self))


#
# Player
#
class Player(Character):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.is_player_controlled = True


#
# AiPlayer
#
class AiPlayer(Character):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)


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

