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

    def kill(self):
        self.on_destroy()
        super().kill()

    def on_init(self):
        pass

    def on_destroy(self):
        pass

    def apply_damage(self, causer: Sprite = None, damage_amount: float = 0):
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

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        for component in self.components:
            component.comp_update(*args, **kwargs)

    def get_component_by_type(self, comp_type):
        found = None
        for c in self.components:
            if c.__class__ == comp_type:
                found = c
                break
        return found


#
# Game Object With Health
#
class GameObjectWithHealth(GameObjectWithComponents):
    def __init__(self, parent: GameObject = None):
        super().__init__(parent)
        self.components.append(HealthComponent(self))

    def apply_damage(self, causer: Sprite = None, damage_amount: float = 0):
        health_component: HealthComponent = self.get_component_by_type(HealthComponent)
        health_component.update_health(damage_amount)


#
# Game Object With Health
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
