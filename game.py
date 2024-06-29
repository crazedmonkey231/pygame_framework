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
        self.level: Level = None
        self._game_components: list[GameComponent] = list()

    # Calculate the delta of a value from the delta time
    def delta_value(self, value) -> float:
        return value * self.delta_time

    # Add game component
    def add_game_component(self, component):
        from game_component import GameComponent
        if isinstance(component, GameComponent):
            self._game_components.append(component)

    # Add game component
    def add_game_component_by_class(self, component_class):
        from game_component import GameComponent
        if issubclass(component_class, GameComponent):
            game_component: GameComponent = component_class(self)
            self._game_components.append(game_component)

    # Remove game component
    def remove_game_component(self, component_to_remove):
        for component in self._game_components:
            if component == component_to_remove:
                component.comp_destroy()
                self._game_components.remove(component)

    # Remove game component by class
    def remove_game_component_by_class(self, component_to_remove):
        for component in self._game_components:
            if component.__class__ == component_to_remove:
                component.comp_destroy()
                self._game_components.remove(component)

    # Remove game component by tag
    def remove_game_component_by_tag(self, comp_tag: str):
        for component in self._game_components:
            if component.comp_tags.__contains__(comp_tag):
                component.comp_destroy()
                self._game_components.remove(component)

    def load_level(self, level):
        from level import Level
        if isinstance(level, Level):
            if self.level:
                self.level.on_unload()
            self.level: Level = level
            self.level.on_load()

    def load_level_by_class(self, level_class):
        from level import Level
        if issubclass(level_class, Level):
            if self.level:
                self.level.on_unload()
            self.level: Level = level_class(self)
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
            if self.level:
                self.level.update_level()
            self.screen.blit(self.background, (0, 0))
            if self.level:
                self.level.draw_level()
            self.screen.blit(self.overlay, (0, 0))
            pygame.display.flip()
            if self.slowdown_factor_max < self.slowdown_factor or self.slowdown_factor < 1:
                self.slowdown_factor = clamp_value(self.slowdown_factor, 1, self.slowdown_factor_max)
            self.delta_time = (self.clock.tick(self.fps) / 1000) / self.slowdown_factor
