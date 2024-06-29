from config import *


#
# Game class
#
class Game(object):
    def __init__(self):
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
        self.level: Level = Level()
        self._game_components: list[GameComponent] = list()

    # Calculate the delta of a value from the delta time
    def delta_value(self, value) -> float:
        return value * self.delta_time

    # Add game component
    def add_game_component(self, component):
        if issubclass(component, GameComponent):
            self._game_components.append(component)

    # Remove game component based on a validation
    def _remove_and_destroy_component(self, validation, component):
        needs_validation = validation if validation is not None else False
        is_valid_comparison = validation == component if needs_validation else False
        if not needs_validation or (needs_validation and is_valid_comparison):
            component.comp_destroy()
            self._game_components.remove(component)

    # Remove game component
    def remove_game_component(self, component_to_remove):
        for component in self._game_components:
            self._remove_and_destroy_component(component, component_to_remove)

    # Remove game component by class
    def remove_game_component_by_class(self, component_to_remove):
        for component in self._game_components:
            self._remove_and_destroy_component(component.__class__, component_to_remove)

    # Remove game component by tag
    def remove_game_component_by_tag(self, comp_tag: str):
        for component in self._game_components:
            if component.comp_tags.__contains__(comp_tag):
                self._remove_and_destroy_component(None, component)

    def load_level(self, level_class):
        if self.level:
            self.level.on_unload()
        self.level = level_class()
        self.level.on_load()

    # Main
    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for component in self._game_components:
                if component.needs_update:
                    component.comp_update()
            self.level.update_level()
            self.screen.blit(self.background, (0, 0))
            self.level.draw_level()
            self.screen.blit(self.overlay, (0, 0))
            pygame.display.flip()
            if self.slowdown_factor_max < self.slowdown_factor or self.slowdown_factor < 1:
                self.slowdown_factor = clamp_value(self.slowdown_factor, 1, self.slowdown_factor_max)
            self.delta_time = (self.clock.tick(self.fps) / 1000) / self.slowdown_factor
