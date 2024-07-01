from config import *

# Configuration
player: Player = Player()
player.add_game_object_component(LightGameObjectComponent)
level: Level = Level(game)
level.add_sprites_to_render([player])
level.add_level_component(DiscoGridLevelComponent)
level.add_level_component(LightGridLevelComponent)
game.load_level(level)

# Initialize game
game.initialize()

# Game loop
while game.running:
    game.game_update()
    pygame.display.flip()

pygame.quit()
