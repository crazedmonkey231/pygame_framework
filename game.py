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
        self.pygame_init_return = pygame.init()
        self.screen: Surface = pygame.display.set_mode((1280, 720))
        self.screen_center = [self.screen.get_width() / 2, self.screen.get_height() / 2]
        self.screen_center_vector2 = Vector2(self.screen_center)
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

    # Add sprites to renderer
    def add_sprites_to_render(self, sprites: list[Sprite]):
        for sprite in sprites:
            self.all_sprites.add(sprite)

    # Get sprites from render layer
    def get_sprites_from_render_layer(self, layer: int = 0):
        return self.all_sprites.get_sprites_from_layer(layer)

    # Calculate the delta of a value from the delta time
    def delta_value(self, value) -> float:
        return value * self.delta_time

    # Image loader
    def load_image(self, name, color_key=None, scale=1):
        fullname = os.path.join(self.data_dir, name)
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pygame.transform.scale(image, size)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image, image.get_rect()

    # Sound loader
    def load_sound(self, name) -> Sound:
        class NoneSound:
            def play(self):
                pass
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = os.path.join(self.data_dir, name)
        sound = pygame.mixer.Sound(fullname)
        return sound

    # Main
    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.all_sprites.update()
            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)
            self.screen.blit(self.overlay, (0, 0))
            pygame.display.flip()
            if not 1 <= self.slowdown_factor <= self.slowdown_factor_max:
                self.slowdown_factor = min(max(self.slowdown_factor, 1), self.slowdown_factor_max)
            self.delta_time = (self.clock.tick(self.fps) / 1000) / self.slowdown_factor
