from config.game_config import *
import random


class EnemySpaceship(pygame.sprite.Sprite):

    def __init__(self):
        # Sprite initialization
        pygame.sprite.Sprite.__init__(self)
        self.image = GameConfig.ENEMY_SPACESHIP_IMG
        self.mask = GameConfig.ENEMY_SPACESHIP_MASK

        # Define initial coordinates
        self.x = GameConfig.ENEMY_SPACESHIP_W + GameConfig.WINDOW_W
        self.y = random.randint(GameConfig.ENEMY_SPACESHIP_H, GameConfig.WINDOW_H - GameConfig.ENEMY_SPACESHIP_H - 20)
        # Define rectangle of the enemy's spaceship
        self.rect = pygame.Rect(self.x, self.y, GameConfig.ENEMY_SPACESHIP_W, GameConfig.ENEMY_SPACESHIP_H)
        # Define horizontal & vertical velocity
        self.vx = GameConfig.FORCE_SHIP_LEFT
        self.vy = 0
        self.tick_animation_spaceship_stopped = 0

    # Update the state of the spaceship
    def advance_state(self): self.rect = self.rect.move(self.vx, self.vy)

    # Draw the spaceship on the frame
    def draw(self, window): window.blit(self.image, self.rect.topleft)

    # Indicates if the spaceship is out of the game frame
    def is_dead(self): return self.rect.right < 0
