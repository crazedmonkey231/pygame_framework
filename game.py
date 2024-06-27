from config import *


#
# Game class
#
class Game(object):
    def __init__(self):
        if not pygame.font:
            print("Warning, fonts disabled")
        if not pygame.mixer:
            print("Warning, sound disabled")
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.data_dir = os.path.join(self.main_dir, 'data')
        self.pygame_init_return: tuple[int, int] = pygame.init()
        self.screen: Surface = pygame.display.set_mode((1280, 720))
        self.screen_center: tuple[float, float] = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.screen_center_vector2: Vector2 = Vector2(self.screen_center)
        self.background: Surface = Surface(self.screen.get_size()).convert()
        self.background.fill([0, 0, 0])
        self.overlay: Surface = Surface(self.screen.get_size()).convert_alpha()
        self.overlay.fill((0, 0, 0, 0))
        self.clock: Clock = Clock()
        self.running: bool = True
        self.fps: int = 120
        self.delta_time: float = 0
        self.slowdown_factor: float = 1
        self.slowdown_factor_max: float = 1000
        self.all_sprites: LayeredUpdates = LayeredUpdates()
        self._game_components: list[GameComponent] = list()

    # Add sprites to renderer
    def add_sprites_to_render(self, sprites: list[Sprite]):
        for sprite in sprites:
            self.all_sprites.add(sprite)

    # Add sprites to renderer with positions
    def add_sprites_to_render_with_pos(self, sprites_list: list[tuple[Sprite, Vector2]]):
        for item in sprites_list:
            sprite, pos = item
            if sprite.rect:
                sprite.rect.center = (pos.x, pos.y)
            self.all_sprites.add(sprite)

    # Get sprites from render layer
    def get_sprites_from_render_layer(self, layer: int = 0) -> list[Sprite]:
        return self.all_sprites.get_sprites_from_layer(layer)

    # Get sprites with positions from render layer
    def get_sprites_from_render_layer_with_pos(self, layer: int = 0) -> list[tuple[Sprite, Vector2]]:
        sprites = self.all_sprites.get_sprites_from_layer(layer)
        return [(sprite, Vector2(sprite.rect.center[0], sprite.rect.center[1])) for sprite in sprites]

    # Calculate the delta of a value from the delta time
    def delta_value(self, value) -> float:
        return value * self.delta_time

    # Image loader
    def load_image(self, name, color_key=None, scale=1) -> tuple[Surface, Rect]:
        image = pygame.image.load(os.path.join(self.data_dir, name)).convert_alpha()
        size = image.get_size()
        image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image, image.get_rect()

    # Sound loader
    def load_sound(self, name) -> object:
        if not mixer_initialized:
            return NoneSound()
        return pygame.mixer.Sound(os.path.join(self.data_dir, name))

    # Add game component
    def add_game_component(self, component):
        if issubclass(component, GameComponent):
            self._game_components.append(component)

    # Remove game component
    def remove_game_component(self, component_to_remove):
        for component in self._game_components:
            if component == component_to_remove:
                self._game_components.remove(component)

    # Remove game component by class
    def remove_game_component_by_class(self, component_to_remove):
        for component in self._game_components:
            if component.__class__ == component_to_remove:
                self._game_components.remove(component)

    # Remove game component by tag
    def remove_game_component_by_tag(self, comp_tag: str):
        for component in self._game_components:
            if component.comp_tags.__contains__(comp_tag):
                self._game_components.remove(component)

    # Main
    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for component in self._game_components:
                component.comp_update()
            self.all_sprites.update()
            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)
            self.screen.blit(self.overlay, (0, 0))
            pygame.display.flip()
            if not 1 <= self.slowdown_factor <= self.slowdown_factor_max:
                self.slowdown_factor = min(max(self.slowdown_factor, 1), self.slowdown_factor_max)
            self.delta_time = (self.clock.tick(self.fps) / 1000) / self.slowdown_factor
