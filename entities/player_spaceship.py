import pygame
import math

from config.game_config import GameConfig
from entities.shot import Shot


class PlayerSpaceship(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Sprite initialization
        pygame.sprite.Sprite.__init__(self)
        # Define rectangle of the player's spaceship
        self.rect = pygame.Rect(x, y, GameConfig.PLAYER_SPACESHIP_W, GameConfig.PLAYER_SPACESHIP_H)  # define rect
        self.image = GameConfig.PLAYER_SPACESHIP_IMG
        self.mask = GameConfig.PLAYER_SPACESHIP_MASK
        # Define horizontal & vertical velocity
        self.vx = 0
        self.vy = 0

        # Define shots' settings
        self.shots = []
        self.shot_cooldown = GameConfig.SHOT_COOLDOWN

        # attributes used to calculate spaceship position
        self.previous_move = None
        self.ticks_keydowned = 0
        self.tick_animation_spaceship_stopped = 0

        # attributs utiles pour le bot
        self.state = 0
        self.previous_move = None
        self.move_ticking = None
        self.move_cooldown = 0
        self.state_0_it = 0
        self.move_stack = []

    # Determine the next coordinates of spaceship according to the move caused by the user's actions
    def get_fx_fy(self, next_move):
        fx, fy = 0, 0
        # Decomposition of the move
        if next_move.left:
            fx = GameConfig.FORCE_SHIP_LEFT
        if next_move.right:
            fx = GameConfig.FORCE_SHIP_RIGHT
        if next_move.up:
            fy = GameConfig.FORCE_SHIP_UP
        if next_move.down:
            fy = GameConfig.FORCE_SHIP_DOWN

        # Idle floating animation by using cos function
        if not next_move.up and not next_move.down and not next_move.right and not next_move.left:
            fy += 2 * math.cos(self.tick_animation_spaceship_stopped / 8)
            self.tick_animation_spaceship_stopped += 1
            if self.tick_animation_spaceship_stopped == 50:
                self.tick_animation_spaceship_stopped = 0

        # Manage linear acceleration if steering is maintained
        if self.previous_move is not None:
            if next_move.up and self.previous_move.up:
                self.ticks_keydowned += 1
                fy -= self.ticks_keydowned * 0.1
            if next_move.down and self.previous_move.down:
                self.ticks_keydowned += 1
                fy += self.ticks_keydowned * 0.1
            if self.previous_move.up and next_move.down:
                self.ticks_keydowned = 0
            if self.previous_move.down and next_move.up:
                self.ticks_keydowned = 0
        if not next_move.up and not next_move.down:
            self.ticks_keydowned = 0

        # Save the move instance to use it in the next game state
        self.previous_move = next_move
        x, y = self.rect.topleft
        # blocking the spaceship in the game frame
        if y + fy > GameConfig.WINDOW_H - GameConfig.PLAYER_SPACESHIP_H:
            fy = 0
        if y + fy < 0:
            fy = 0
        if x + fx < 0:
            fx = 0
        if x + fx > GameConfig.WINDOW_W - GameConfig.PLAYER_SPACESHIP_W:
            fx = 0
        return fx, fy

    # Manage action related to spaceship's shots
    def shoot_action(self, next_move):
        # Manage shots according to cooldown
        if next_move.shoot and self.shot_cooldown == 0:
            self.shots.append(Shot(self.rect.right, self.rect.centery))
            self.shot_cooldown = GameConfig.SHOT_COOLDOWN
        elif self.shot_cooldown > 0:
            self.shot_cooldown -= 1

        # Advancement of shots on the screen and destruction of if it is out of the screen
        for shot in self.shots:
            shot.advance_state()
            if shot.is_dead():
                self.shots.remove(shot)

    # Update the state of the spaceship
    def advance_state(self, next_move, game_state):
        self.vx, self.vy = self.get_fx_fy(next_move)
        self.shoot_action(next_move)
        self.rect = self.rect.move(self.vx, self.vy)

    # Draw the spaceship on the frame
    def draw(self, window): window.blit(self.image, self.rect.topleft)

    # Indicates if the spaceship is collides an asteroid
    def is_touching(self, asteroid): return pygame.sprite.collide_mask(self, asteroid)
