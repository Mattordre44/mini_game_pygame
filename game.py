import sys
import time

from bot import Bot
from entities.player_spaceship import PlayerSpaceship
from game_state import *
from config.move import *


# Allows to catch user's keyboard interactions and therefore determine the desired motion + shoots
def get_next_move():
    next_move = Move()
    keys = pygame.key.get_pressed()
    next_move.up = keys[pygame.K_UP]
    next_move.down = keys[pygame.K_DOWN]
    next_move.left = keys[pygame.K_LEFT]
    next_move.right = keys[pygame.K_RIGHT]
    next_move.shoot = keys[pygame.K_w]
    return next_move


# Manage the game loop which is executed every 20ms
def game_loop(window, activate_bot):
    if activate_bot:
        spaceship = Bot(130, 130)
    else:
        spaceship = PlayerSpaceship(130, 130)
    game_state = GameState(spaceship)
    x_background = 0
    quitting = False
    game_over = False
    while not game_over and not quitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        next_move = get_next_move()
        game_state.advance_state(next_move)
        game_state.draw_background(window, x_background)
        game_state.draw(window)
        x_background -= GameConfig.BACKGROUND_SCROLL_SPEED

        display_score_message(window, game_state)
        pygame.time.delay(20)

        if game_state.is_over():
            display_loose_message(window)
            game_over = True
        pygame.display.update()
    if not quitting:
        if play_again():
            game_loop(window, activate_bot)


# Manage the decision of the player to play again or quit the game
# -> by default after 10 seconds it restart a game
def play_again():
    t_end = time.time() + 10
    while time.time() < t_end:
        for event in pygame.event.get([pygame.KEYDOWN, pygame.QUIT]):
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                pygame.time.delay(500)
                return True
    return True


# Display the actual score of the game
def display_score_message(window, game_state):
    text = GameConfig.NORMAL_FONT.render('Score : ' + str(game_state.score), True, GameConfig.YELLOW)
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    window.blit(text, text_rect)


# Display a message when the game is over
def display_loose_message(window):
    text_1 = GameConfig.TITLE_FONT.render('Game over', True, GameConfig.YELLOW)
    text_1_rect = text_1.get_rect()
    text_1_rect.center = (GameConfig.WINDOW_W / 2, GameConfig.WINDOW_H / 2)
    window.blit(text_1, text_1_rect)
    text_2 = GameConfig.NORMAL_FONT.render('You will win this intergalactic battle next time !', True, GameConfig.YELLOW)
    text_2_rect = text_2.get_rect()
    text_2_rect.center = (GameConfig.WINDOW_W / 2, GameConfig.WINDOW_H / 2 + 80)
    window.blit(text_2, text_2_rect)
    text_3 = GameConfig.NORMAL_FONT.render('Press a key to play again :)', True, GameConfig.YELLOW)
    text_3_rect = text_3.get_rect()
    text_3_rect.center = (GameConfig.WINDOW_W / 2, GameConfig.WINDOW_H / 2 + 110)
    window.blit(text_3, text_3_rect)


# Main function which is the entry point of the game
def main():
    activate_bot = sys.argv.__contains__("-bot")
    pygame.init()
    window = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H))
    GameConfig.init()
    pygame.display.set_caption("Galactic War")
    game_loop(window, activate_bot)
    pygame.quit()
    quit()


main()
