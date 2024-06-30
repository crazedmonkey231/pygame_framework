from config import *


#
# Grid Level component
#
class GridLevelComponent(LevelComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_size: Vector2 = Vector2(24, 24)
        self.grid_slot_width = self.parent.parent.screen_size_vector2.x / self.grid_size.x
        self.grid_slot_width_half = self.grid_slot_width / 2
        self.grid_slot_height = self.parent.parent.screen_size_vector2.y / self.grid_size.y
        self.grid_slot_height_half = self.grid_slot_height / 2
