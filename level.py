from config import *


#
# Level
#
class Level(object):
    def __init__(self, parent: Game):
        self.parent: Game = parent
        self._all_sprites: LayeredUpdates = LayeredUpdates()
        self._level_components: list[LevelComponent] = list()

    # On load
    def load(self):
        activate_components(self._level_components)

    # On unload
    def unload(self):
        deactivate_components(self._level_components)

    def destroy(self):
        destroy_components(self._level_components)

    def reset(self):
        reset_components(self._level_components)

    # Update all sprites
    def update(self):
        update_components(self._level_components)
        self._all_sprites.update()

    # Draw all sprites
    def draw(self):
        draw_components(self._level_components)
        self._all_sprites.draw(self.parent.screen)

    # Add level component
    def add_level_component(self, component):
        from component import LevelComponent
        add_component(LevelComponent, self._level_components, component, self)

    # Remove level component
    def remove_level_component(self, component, optional_tags: set[str] = None):
        from component import LevelComponent
        remove_component(LevelComponent, self._level_components, component, optional_tags)

    # Add sprites to renderer
    def add_sprites_to_render(self, sprites: list[Sprite]):
        for sprite in sprites:
            self._all_sprites.add(sprite)

    # Add sprites to renderer with positions
    def add_sprites_to_render_with_pos(self, sprites_list: list[tuple[Sprite, Vector2]]):
        for item in sprites_list:
            sprite, pos = item
            if sprite.rect:
                sprite.rect.center = (pos.x, pos.y)
            self._all_sprites.add(sprite)

    def remove_sprites_from_render(self, sprites: list[Sprite]):
        self._all_sprites.remove(sprites)

    # Get sprites from render layer
    def get_sprites_from_render_layer(self, layer: int = 0) -> list[Sprite]:
        return self._all_sprites.get_sprites_from_layer(layer)

    # Get sprites with positions from render layer
    def get_sprites_from_render_layer_with_pos(self, layer: int = 0) -> list[tuple[Sprite, Vector2]]:
        sprites = self._all_sprites.get_sprites_from_layer(layer)
        return [(sprite, Vector2(sprite.rect.center)) for sprite in sprites]

    # Get sprites with positions from render layer
    def get_sprites_from_render_layer_within_distance(self, game_object: GameObject, distance: float = 100,
                                                      layer: int = 0) -> list[Sprite]:
        sprites = self._all_sprites.get_sprites_from_layer(layer)
        return [sprite for sprite in sprites if game_object.distance_to_game_object(sprite) <= distance]
