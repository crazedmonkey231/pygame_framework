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
        if component:
            if isinstance(component, GameComponent):
                self._game_components.append(component)
            if issubclass(component, GameComponent):
                game_component: GameComponent = component(self)
                self._game_components.append(game_component)

    # Remove game component
    def remove_game_component(self, component, optional_tags: set[str] = None):
        from game_component import GameComponent
        if component or optional_tags:
            for gc in self._game_components:
                f1 = (component and ((isinstance(component, GameComponent) and gc == component) or
                                     (issubclass(component, GameComponent) and gc.__class__ == component)))
                f2 = optional_tags and bool(gc.comp_tags & optional_tags)
                if f1 or f2:
                    gc.comp_destroy()
                    self._game_components.remove(gc)

    def load_level(self, level):
        from level import Level
        if self.level:
            self.level.on_unload()
        if isinstance(level, Level):
            self.level: Level = level
        if issubclass(level, Level):
            self.level: Level = level(self)
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
                self.level.draw_level()
                self.screen.blit(self.overlay, (0, 0))
                pygame.display.flip()
            if self.slowdown_factor_max < self.slowdown_factor or self.slowdown_factor < 1:
                self.slowdown_factor = clamp_value(self.slowdown_factor, 1, self.slowdown_factor_max)
            self.delta_time = (self.clock.tick(self.fps) / 1000) / self.slowdown_factor
