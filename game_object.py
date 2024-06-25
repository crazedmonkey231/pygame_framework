from config import *


#
# Game Object
#
class GameObject(Sprite):
    def __init__(self, parent=None):
        Sprite.__init__(self)
        self.on_init()
        self.parent = parent
        self.layer: int = 0
        self.tags: set[str] = set()

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
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.components: list[GameObjectComponent] = list()

    def on_destroy(self):
        super().on_destroy()
        self.components.clear()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        for component in self.components:
            if component.needs_update:
                component.comp_update(*args, **kwargs)

    def get_component_by_type(self, comp_type):
        for component in self.components:
            if component.__class__ == comp_type:
                return component
        return None


#
# Game Object With Movement
#
class GameObjectWithMovement(GameObjectWithComponents):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.components.append(MovementComponent)


#
# Game Object With Health
#
class GameObjectWithHealth(GameObjectWithMovement):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.components.append(HealthComponent(self))

    def apply_damage(self, causer: Sprite = None, damage_amount: float = 0):
        super().apply_damage(causer, damage_amount)
        health_component: HealthComponent = self.get_component_by_type(HealthComponent)
        health_component.update_health(damage_amount)


#
# Game Object With Timer
#
class GameObjectWithTimer(GameObjectWithHealth):
    def __init__(self, parent: GameObject = None, time_to_live: float = 0):
        super().__init__(parent)
        self.components.append(CountDownComponent(self, time_to_live))


#
# Character
#
class Character(GameObjectWithHealth):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.is_player_controlled: bool = False


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


#
# Effect
#
class Effect(GameObjectWithHealth):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)


#
# Effect With Timer
#
class EffectWithTimer(GameObjectWithTimer):
    def __init__(self, parent: GameObject = None, time_to_live: float = 0):
        super().__init__(parent, time_to_live)


#
# Widget
#
class Widget(GameObjectWithHealth):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)


#
# Widget With Timer
#
class WidgetWithTimer(GameObjectWithTimer):
    def __init__(self, parent: GameObject = None, time_to_live: float = 0):
        super().__init__(parent, time_to_live)
