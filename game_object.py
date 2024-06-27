from config import *


#
# Game Object
#
class GameObject(Sprite):
    def __init__(self, parent=None):
        Sprite.__init__(self)
        self.on_init()
        self.parent = parent
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
    def __init__(self, parent: GameObject = None, components: list[GameObjectComponent] = None):
        super().__init__(parent)
        if components is None:
            self._components = list()
        else:
            self._components = components
            for component in self._components:
                component.comp_init()

    def on_destroy(self):
        super().on_destroy()
        for components in self._components:
            components.comp_destroy()
        self._components.clear()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        for component in self._components:
            if component.needs_update:
                component.comp_update(*args, **kwargs)

    def get_component_by_class(self, comp_class):
        for component in self._components:
            if component.__class__ == comp_class:
                return component
        return None

    def add_game_component(self, component: GameObjectComponent):
        self._components.append(component)

    def remove_game_component(self, component_to_remove: GameObjectComponent):
        for component in self._components:
            if component == component_to_remove:
                self._components.remove(component)
                component.comp_destroy()

    def remove_game_component_by_class(self, component_to_remove):
        for component in self._components:
            if component.__class__ == component_to_remove:
                self._components.remove(component)
                component.comp_destroy()

    def remove_game_component_by_tag(self, comp_tag: str):
        for component in self._components:
            if component.comp_tags.__contains__(comp_tag):
                self._components.remove(component)
                component.comp_destroy()

    def apply_damage(self, causer: Sprite = None, damage_amount: float = 0):
        super().apply_damage(causer, damage_amount)
        health_component: HealthComponent = self.get_component_by_class(HealthComponent)
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


# ----------------------------------------------------------------------------------------------------------------------

#
# Sound
#
class NoneSound(object):
    def play(self):
        pass
