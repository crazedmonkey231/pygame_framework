from config import *

# Configuration
level: Level = Level(game)
level.add_level_component(DiscoGridLevelComponent)
game.load_level(level)

# Initialize game
game.initialize()

# Game loop
while game.running:
    game.game_update()
    pygame.display.flip()

pygame.quit()
