import pygame
from config.game_config import GameConfig


class Explosion:
    def __init__(self, pos, cent):
        # Load different images of the Explosion
        self.images = GameConfig.EXPLOSION_IMGS

        # Define the animation counter from 1 -> 6
        self.animation_count = 0

        # define rectangle of the explosion
        self.rect = pygame.Rect(pos[0], pos[1], GameConfig.EXPLOSION_W, GameConfig.EXPLOSION_H)

        # center the rectangle on the center of explosion object
        self.rect.center = cent

    # Update the state of the asteroid
    def advance_state(self): self.animation_count += 1

    # Draw the explosion on the frame
    def draw(self, window): window.blit(self.images[self.animation_count], self.rect.topleft)

    # Indicates if the last animation rate has been displayed
    def is_dead(self): return self.animation_count > 6
