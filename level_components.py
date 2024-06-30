from config import *


#
# Grid Level component
#
class GridLevelComponent(LevelComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.tile_size: int = 16
        self.tile_size_half: float = self.tile_size / 2
        self.tile_size_vector2 = Vector2(self.tile_size, self.tile_size)
        self.num_tiles_x: int = int(self.parent.parent.screen_size_vector2.x // self.tile_size)
        self.num_tiles_y: int = int(self.parent.parent.screen_size_vector2.y // self.tile_size)
        self.grid_slots: list[GridSlotGameObject] = list()

    def _grid_update(self):
        pass

    def comp_update(self):
        super().comp_update()
        if self.grid_slots:
            self._grid_update()

    def comp_activate(self):
        super().comp_activate()
        grid: list[tuple[GridSlotGameObject, Vector2]] = list()
        for row in range(self.num_tiles_y):
            for col in range(self.num_tiles_x):
                grid_slot_game_object: GridSlotGameObject = GridSlotGameObject(self.tile_size_vector2)
                center_pos: Vector2 = Vector2((col * self.tile_size + self.tile_size_half,
                                               row * self.tile_size + self.tile_size_half))
                grid.append((grid_slot_game_object, center_pos))
                self.grid_slots.append(grid_slot_game_object)
        self.parent.add_sprites_to_render_with_pos(grid)

    def comp_deactivate(self):
        super().comp_deactivate()
        for slot in self.grid_slots:
            slot.kill()
        self.grid_slots.clear()


class DiscoGridLevelComponent(GridLevelComponent):
    def __init__(self, parent):
        super().__init__(parent)

    def _grid_update(self):
        super()._grid_update()
        new_background_color = (random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255),
                                255)
        random_index = random.randint(0, len(self.grid_slots) - 1)
        grid_slot = self.grid_slots[random_index]
        grid_slot.background_color = new_background_color

        dist_to_center = clamp_value(255 - (255 - grid_slot.distance_to_position(self.game.screen_center) * 2), 0, 255)

        new_overlay_color = (0, 0, 0, dist_to_center)
        grid_slot.overlay_color = new_overlay_color
