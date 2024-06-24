from config import *


#
# Game Object Component
#
class GameObjectComponent(object):
    def __init__(self, parent: GameObjectWithComponents):
        self.parent = parent

    def comp_update(self, *args, **kwargs):
        pass


#
# Health Component
#
class HealthComponent(GameObjectComponent):
    def __init__(self, parent: GameObjectWithComponents, health: float = 100, max_health: float = 100,
                 health_update_change: float = 0):
        super().__init__(parent)
        self.health: float = health
        self.health_max: float = max_health
        self.health_update_change: float = health_update_change

    def update_health(self, amount: float):
        self.health = min(max(self.health + amount, 0), self.health_max)
        if not self.health:
            self.parent.kill()

    def comp_update(self):
        super().comp_update()
        if not self.health_update_change != 0:
            self.update_health(self.health_update_change)


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

    def comp_update(self):
        pass


#
# Count Down Component
#
class CountDownComponent(GameObjectComponent):
    def __init__(self, parent: GameObjectWithComponents, time_to_live: float = 10):
        super().__init__(parent)
        self.parent: GameObjectWithComponents = parent
        self.time_to_live: float = time_to_live

    def comp_update(self):
        self.time_to_live -= game.delta_time
        if 0 >= self.time_to_live:
            self.parent.apply_damage(self.parent, -999999)
