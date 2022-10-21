import random
import pygame

from entities.asteroid import Asteroid
from config.game_config import GameConfig
from entities.enemy_spaceship import EnemySpaceship
from entities.explosion import Explosion


class GameState:

    def __init__(self, spaceship):
        # Game spaceship, could be a bot of controlled by the player
        self.spaceship = spaceship
        # Score of the game
        self.score = 0
        # list of asteroids on the game frame
        self.asteroids = []
        # Constant defining the time between the spawn of 2 asteroids
        self.time_till_new_asteroid = GameConfig.TICK_BETWEEN_ASTEROID
        # list of enemy spaceships on the game frame
        self.enemy_spaceships = []
        # Constant defining the time between the spawn of 2 enemy spaceships
        self.enemy_ship_cooldown = GameConfig.ENEMY_SPAWN_COOLDOWN
        # list of explosions that appears on the game frame
        self.explosions = []

    # Draw all the game's elements on the frame
    def draw(self, window):
        self.spaceship.draw(window)

        for shot in self.spaceship.shots:
            shot.draw(window)

        for asteroid in self.asteroids:
            asteroid.draw(window)

        for enemy in self.enemy_spaceships:
            enemy.draw(window)

        for explosion in self.explosions:
            explosion.draw(window)

    @staticmethod
    # Draw the background in motion
    def draw_background(window, x):
        rel_x = x % GameConfig.BACKGROUND_W
        window.blit(GameConfig.BACKGROUND_IMG, (rel_x - GameConfig.BACKGROUND_W, 0))
        if rel_x < GameConfig.WINDOW_W:
            window.blit(GameConfig.BACKGROUND_IMG, (rel_x, 0))

    # Update the state of the game
    def advance_state(self, next_move):
        for asteroid in self.asteroids:
            for shot in self.spaceship.shots:

                # If a shot is colliding an asteroid
                if pygame.sprite.collide_mask(asteroid, shot):
                    if asteroid.lives == 0:
                        # The asteroid is dead -> add an explosion and increase the score
                        self.explosions.append(Explosion(asteroid.rect.topleft, asteroid.rect.center))
                        self.asteroids.remove(asteroid)
                        self.spaceship.shots.remove(shot)
                        self.score += 1
                    else:
                        # The asteroid is loosing a life
                        self.spaceship.shots.remove(shot)
                        asteroid.lives -= 1
            asteroid.advance_state()

            if asteroid.is_dead():
                self.asteroids.remove(asteroid)
                self.score += 1

        # allows at least one asteroid to be present on the game frame
        if len(self.asteroids) == 0:
            asteroid = Asteroid()
            self.asteroids.append(asteroid)

        # randomly creating a new asteroid -> there is a maximum of 2
        if 2 > len(self.asteroids) >= 1:
            if self.time_till_new_asteroid == 0:
                self.time_till_new_asteroid = GameConfig.TICK_BETWEEN_ASTEROID
                if random.choice([True, False]):
                    self.asteroids.append(Asteroid())
        elif self.time_till_new_asteroid == 0:
            self.time_till_new_asteroid = GameConfig.TICK_BETWEEN_ASTEROID

        # Update state of player's spaceship
        self.spaceship.advance_state(next_move, self)

        if self.enemy_ship_cooldown == 0:
            self.enemy_spaceships.append(EnemySpaceship())
            self.enemy_ship_cooldown = GameConfig.ENEMY_SPAWN_COOLDOWN
        else:
            self.enemy_ship_cooldown -= 1

        # If a shot is colliding an enemy spaceship
        for enemy in self.enemy_spaceships:
            enemy.advance_state()
            if enemy.is_dead():
                self.enemy_spaceships.remove(enemy)
            for shot in self.spaceship.shots:
                if pygame.sprite.collide_mask(enemy, shot):
                    self.explosions.append(Explosion(enemy.rect.topleft, enemy.rect.center))
                    self.enemy_spaceships.remove(enemy)
                    self.score += 5
                    self.spaceship.shots.remove(shot)

        # Update state of explosions
        for explosion in self.explosions:
            explosion.advance_state()
            if explosion.is_dead():
                self.explosions.remove(explosion)

        self.time_till_new_asteroid -= 1

    # Determines if the game is over
    def is_over(self):
        # Is the spaceship touching an asteroid
        for asteroid in self.asteroids:
            if self.spaceship.is_touching(asteroid):
                return True
        # Is the spaceship touching an enemy spaceship
        for enemy in self.enemy_spaceships:
            if pygame.sprite.collide_mask(self.spaceship, enemy):
                return True
        return False
