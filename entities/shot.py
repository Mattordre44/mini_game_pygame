from config.game_config import GameConfig
import pygame


class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Sprite initialization
        pygame.sprite.Sprite.__init__(self)
        # Define rectangle of the shot
        self.rect = pygame.Rect(x, y, GameConfig.SHOT_W, GameConfig.SHOT_H)
        self.vx = GameConfig.SHOT_SPEED
        self.image = GameConfig.SHOT_IMG

    # Update the state of the shot
    def advance_state(self): self.rect = self.rect.move(self.vx, 0)

    # Draw the shot on the frame
    def draw(self, window): window.blit(self.image, self.rect.topleft)

    # Indicates if the shot is out of the game frame
    def is_dead(self): return self.rect.left > GameConfig.WINDOW_W
