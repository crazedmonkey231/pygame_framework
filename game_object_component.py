from config import *


#
# Game Object Component
#
class GameObjectComponent(object):
    def __init__(self, parent: GameObjectWithComponents):
        self.parent = parent
        self.needs_update = True

    def comp_update(self, *args, **kwargs):
        pass


#
# Health Component
#
class HealthComponent(GameObjectComponent):
    def __init__(self, parent: GameObjectWithComponents, health: float = 100, health_max: float = 100,
                 health_update_change: float = 0):
        super().__init__(parent)
        self.health: float = health
        self.health_max: float = min(health_max, config_health_max)
        self.health_update_change: float = health_update_change

    def update_health(self, amount: float):
        self.health = min(max(self.health + amount, 0), self.health_max, config_health_max)
        if not self.health:
            self.parent.kill()

    def comp_update(self, *args, **kwargs):
        super().comp_update(*args, **kwargs)
        if not self.health_update_change != 0:
            self.update_health(self.health_update_change)


#
# Movement Component
#
class MovementComponent(GameObjectComponent):
    def __init__(self, parent: GameObjectWithComponents, move_speed: Vector2 = Vector2(0, 0)):
        super().__init__(parent)
        self.move_speed: Vector2 = move_speed
        self.velocity = Vector2(0, 0)

    def comp_update(self, *args, **kwargs):
        super().comp_update(*args, **kwargs)
        center = self.parent.rect.center
        center_x = center[0] + game.delta_value(self.move_speed.x)
        center_y = center[1] + game.delta_value(self.move_speed.y)
        self.parent.rect.center = (center_x, center_y)
        self.velocity = Vector2(center_x - center[0], center_y - center[1])


#
# Count Down Component
#
class CountDownComponent(GameObjectComponent):
    def __init__(self, parent: GameObjectWithComponents, time_to_live: float = 10):
        super().__init__(parent)
        self.time_to_live: float = time_to_live

    def comp_update(self, *args, **kwargs):
        super().comp_update(*args, **kwargs)
        self.time_to_live -= game.delta_time
        if 0 >= self.time_to_live:
            if self.parent.get_component_by_type(HealthComponent):
                self.parent.apply_damage(self.parent, -config_health_max)
            else:
                self.parent.kill()


#
# Power Up Tracker Component
#
class PowerTrackerComponent(GameObjectComponent):
    def __init__(self, parent: GameObjectWithComponents):
        super().__init__(parent)
        self.parent: GameObjectWithComponents = parent
        self.total_power: float = 0

    def is_active(self):
        return self.total_power == 100

    def update_power(self, amount: float):
        self.total_power = min(max(self.total_power + amount, 0), 100)

    def comp_update(self, *args, **kwargs):
        super().comp_update(*args, **kwargs)
