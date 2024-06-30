from component import *


#
# Health Component
#
class HealthComponent(GameObjectComponent):
    def __init__(self, parent, health: float = 100, health_max: float = 100,
                 health_update_change: float = 0):
        super().__init__(parent)
        self.health: float = health
        self.health_max: float = min(health_max, config_health_max)
        self.health_update_change: float = health_update_change

    def update_health(self, amount: float):
        self.health = clamp_value(self.health + amount, 0, self.health_max)
        if not self.health:
            self.parent.kill()

    def comp_update(self):
        super().comp_update()
        if not self.health_update_change != 0:
            self.update_health(self.health_update_change)


#
# Movement Component
#
class MovementComponent(GameObjectComponent):
    def __init__(self, parent, move_speed: Vector2 = Vector2(0, 0)):
        super().__init__(parent)
        self.move_speed: Vector2 = move_speed
        self.velocity: Vector2 = Vector2(0, 0)

    def comp_update(self):
        super().comp_update()
        rect = self.parent.rect
        center = rect.center
        center_x = center[0] + self.game.delta_value(self.move_speed.x)
        center_y = center[1] + self.game.delta_value(self.move_speed.y)
        self.parent.rect.center = (center_x, center_y)
        self.velocity = Vector2(center_x - center[0], center_y - center[1])


#
# Count Down Component
#
class CountDownComponent(GameObjectComponent):
    def __init__(self, parent, time_to_live: float = 10, should_destroy: bool = True):
        super().__init__(parent)
        self.countdown_active: bool = True
        self.should_destroy: bool = should_destroy
        self.time_to_live: float = time_to_live

    def reset_countdown(self, time_to_live: float = 10, should_destroy: bool = True):
        self.time_to_live: float = time_to_live
        self.should_destroy = should_destroy
        self.countdown_active = True
        self.needs_update = True

    def on_countdown_end(self):
        if self.should_destroy:
            if get_component_by_class(self.parent.get_components(), HealthComponent):
                self.parent.apply_damage(self.parent, -config_health_max)
            else:
                self.parent.kill()
        self.time_to_live = 0
        self.countdown_active = False
        self.needs_update = False

    def comp_update(self):
        super().comp_update()
        if self.countdown_active:
            self.time_to_live -= self.game.delta_time
            if 0 >= self.time_to_live:
                self.on_countdown_end()


#
# Power Up Tracker Component
#
class PowerTrackerComponent(GameObjectComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.total_power: float = 0

    def is_active(self):
        return self.total_power == 100

    def update_power(self, amount: float):
        self.total_power = clamp_value(self.total_power + amount, 0, 100)

    def comp_update(self):
        super().comp_update()


#
# Game Object Holder Component
#
class GameObjectHolder(GameObjectComponent):
    def __init__(self, parent, held_game_object):
        super().__init__(parent)
        self.held_game_object: GameObject = held_game_object if isinstance(held_game_object, GameObject) else None
        self.needs_update = False

    def _hold_game_object(self):
        if self.held_game_object:
            self.held_game_object.rect.center = self.parent.rect.center

    def comp_activate(self):
        super().comp_activate()
        self._hold_game_object()

    def comp_update(self):
        super().comp_update()
        self._hold_game_object()

    def comp_reset(self):
        super().comp_reset()
        self._hold_game_object()

    def comp_deactivate(self):
        super().comp_deactivate()
        self.held_game_object = None

    def comp_destroy(self):
        super().comp_destroy()
        self.held_game_object = None


#
# Light
#
class Light(GameObjectComponent):
    def __init__(self, parent):
        super().__init__(parent)
