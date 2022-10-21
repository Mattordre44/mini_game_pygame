import pygame


class GameConfig:

    # Constantes
    WINDOW_H = 600
    WINDOW_W = 1100

    BACKGROUND_IMG = None
    BACKGROUND_W = 1024

    ASTEROID_IMGS = None
    ASTEROID_MASK = None
    ASTEROID_1_W = 100
    ASTEROID_1_H = 100

    TICK_BETWEEN_ASTEROID = 200

    ASTEROID_LIFES = 3

    BACKGROUND_SCROLL_SPEED = 0.5

    PLAYER_SPACESHIP_W = 128
    PLAYER_SPACESHIP_H = 68

    PLAYER_SPACESHIP_IMG = None
    PLAYER_SPACESHIP_MASK = None

    ENEMY_SPACESHIP_W = 64
    ENEMY_SPACESHIP_H = 32

    ENEMY_SPACESHIP_IMG = None
    ENEMY_SPACESHIP_MASK = None

    FORCE_SHIP_RIGHT = 6
    FORCE_SHIP_LEFT = -6
    FORCE_SHIP_UP = -6
    FORCE_SHIP_DOWN = 6

    SHOT_SPEED = 10

    SHOT_IMG = None

    SHOT_H = 2
    SHOT_W = 8

    SHOT_COOLDOWN = 20

    ENEMY_SPAWN_COOLDOWN = 200

    EXPLOSION_IMGS = None

    EXPLOSION_W = 150
    EXPLOSION_H = 150

    TITLE_FONT = None
    NORMAL_FONT = None

    WHITE = (255, 255, 255)
    YELLOW = (239, 232, 20)

    BOT_THRESHOLD = 100
    BOT_MOVE_COOLDOWN = 5

    @staticmethod
    def init():
        GameConfig.BACKGROUND_IMG = pygame.image.load('ressources/space.png')

        GameConfig.PLAYER_SPACESHIP_IMG = pygame.image.load('ressources/spaceship_purple.png').convert_alpha()
        GameConfig.PLAYER_SPACESHIP_MASK = pygame.mask.from_surface(GameConfig.PLAYER_SPACESHIP_IMG)

        GameConfig.SHOT_IMG = pygame.image.load('ressources/rocket_spaceship.png').convert_alpha()

        GameConfig.ASTEROID_IMGS = [
            pygame.image.load('ressources/asteroid/asteroid_1_4.png').convert_alpha(),
            pygame.image.load('ressources/asteroid/asteroid_2_4.png').convert_alpha(),
            pygame.image.load('ressources/asteroid/asteroid_3_4.png').convert_alpha(),
            pygame.image.load('ressources/asteroid/asteroid_4_4.png').convert_alpha()
        ]

        GameConfig.ASTEROID_MASK = pygame.mask.from_surface(GameConfig.ASTEROID_IMGS[0])

        GameConfig.ENEMY_SPACESHIP_IMG = pygame.image.load('ressources/spaceship_red.png').convert_alpha()
        GameConfig.ENEMY_SPACESHIP_IMG = pygame.transform.scale(GameConfig.ENEMY_SPACESHIP_IMG, (64, 32))
        GameConfig.ENEMY_SPACESHIP_MASK = pygame.mask.from_surface(GameConfig.ENEMY_SPACESHIP_IMG)

        GameConfig.EXPLOSION_IMGS = [
            pygame.image.load('ressources/explosion/explosion1.png').convert_alpha(),
            pygame.image.load('ressources/explosion/explosion2.png').convert_alpha(),
            pygame.image.load('ressources/explosion/explosion3.png').convert_alpha(),
            pygame.image.load('ressources/explosion/explosion4.png').convert_alpha(),
            pygame.image.load('ressources/explosion/explosion5.png').convert_alpha(),
            pygame.image.load('ressources/explosion/explosion6.png').convert_alpha(),
            pygame.image.load('ressources/explosion/explosion7.png').convert_alpha()
        ]

        GameConfig.NORMAL_FONT = pygame.font.Font('ressources/font/Titania-Regular.ttf', 20)
        GameConfig.TITLE_FONT = pygame.font.Font('ressources/font/Titania-Regular.ttf', 160)
