from config import *


#
# Game class
#
class Game(object):
    def __init__(self):
        self.screen_size: tuple[int, int] = (240, 240)
        self.screen_size_vector2: Vector2 = Vector2(self.screen_size)
        self.screen: Surface = pygame.display.set_mode(self.screen_size)
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
        from component import GameComponent
        add_component(GameComponent, self._game_components, component, self)

    # Remove game component
    def remove_game_component(self, component, optional_tags: set[str] = None):
        from component import GameComponent
        remove_component(GameComponent, self._game_components, component, optional_tags)

    def load_level(self, level):
        from level import Level
        if self.level:
            self.level.unload()
            self.level.destroy()
        if isinstance(level, Level):
            self.level: Level = level
        elif isinstance(level, type) and issubclass(level, Level):
            self.level: Level = level(self)
        if self.level:
            self.level.load()

    def game_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        update_components(self._game_components)
        self.level.update()
        self.screen.blit(self.background, (0, 0))
        draw_components(self._game_components)
        self.level.draw()
        self.screen.blit(self.overlay, (0, 0))
        if self.slowdown_factor_max < self.slowdown_factor or self.slowdown_factor < 1:
            self.slowdown_factor = clamp_value(self.slowdown_factor, 1, self.slowdown_factor_max)
        self.delta_time = (self.clock.tick(self.fps) / 1000) / self.slowdown_factor
