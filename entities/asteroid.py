from random import randint

import pygame

from config.game_config import GameConfig


class Asteroid(pygame.sprite.Sprite):

    def __init__(self):
        # Sprite initialization
        pygame.sprite.Sprite.__init__(self)

        # Randomly generate the initial ordinate
        y = randint(0, GameConfig.WINDOW_H - GameConfig.ASTEROID_1_H)

        # Define rectangle of the Asteroid
        self.rect = pygame.Rect(GameConfig.WINDOW_W, y, GameConfig.ASTEROID_1_W, GameConfig.ASTEROID_1_H)

        # Load different images of the asteroid
        self.image = GameConfig.ASTEROID_IMGS

        # Load the mask of the asteroid
        self.mask = GameConfig.ASTEROID_MASK

        # Define horizontal velocity
        self.vx = -1

        # Define vertical velocity
        self.vy = 0

        # Define asteroid's life counter from 0 -> 3
        self.lives = GameConfig.ASTEROID_LIFES

    # Update the state of the asteroid
    def advance_state(self): self.rect = self.rect.move(self.vx, 0)

    # Draw the asteroid on the frame
    def draw(self, window): window.blit(self.image[self.lives], self.rect.topleft)

    # Indicates if an asteroid is out of the game frame
    def is_dead(self): return self.rect.right <= 0
