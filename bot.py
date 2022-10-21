import math
from entities.player_spaceship import PlayerSpaceship
from config.game_config import GameConfig
from config.move import Move
from random import shuffle


# Take a list of Move and return an opposed one
def get_opposite_path(moves_list: list[Move]):
    res = []
    move_up = Move()
    move_down = Move()
    move_up.up = True
    move_down.down = True
    for i in range(0, len(list)):
        if moves_list[i].down:
            res.append(move_up)
        elif moves_list[i].up:
            res.append(move_down)
        else:
            res.append(Move())
    return res


# Retrives the distance between 2 objects
def get_distance_between_to_object(obj1, obj2):
    x1, y1 = obj1.rect.centerx, obj1.rect.right
    x2, y2 = obj2.rect.centerx, obj2.rect.left
    dist = (y2 - y1) ** 2 + (x2 - x1) ** 2
    dist = math.sqrt(dist)
    return dist


# Determines if there is a conflit following y-axis between objects 1 and 2
def is_in_conflict_y(obj1, obj2):
    return (
            obj2.rect.top < obj1.rect.top < obj2.rect.bottom or
            obj2.rect.top < obj1.rect.bottom < obj2.rect.bottom or
            obj1.rect.top < obj2.rect.center[1] < obj1.rect.bottom
    )


# Determines if there is a conflit following x-axis between objects 1 and 2
def is_in_conflict_x(obj1, seuil, obj2):
    return (obj1.rect.left + seuil + GameConfig.PLAYER_SPACESHIP_W) >= obj2.rect.left


# Determines if 2 objects are in conflicts
def is_in_conflict(obj1, seuil, obj2):
    return is_in_conflict_x(obj1, seuil, obj2) and is_in_conflict_y(obj1, obj2)


# Determines the coordinates of the impact point between the 2 objects
def get_intersection_with_bot(spaceship, obj2, threshold):
    # Store current data
    obj1_tmp = PlayerSpaceship(spaceship.rect.x, spaceship.rect.y)
    obj2_tmp = obj2
    x_spaceship = obj1_tmp.rect.right
    y_spaceship = obj1_tmp.rect.center[1]
    x_obj = obj2.rect.left
    y_obj = obj2.rect.center[1]
    vx_obj = obj2.vx
    vy_obj = obj2.vy
    coord_tmp_spaceship = [x_spaceship, y_spaceship]
    coord_tmp_obj = [x_obj, y_obj]
    counter_y = 0

    # If the player spaceship is above the object
    if y_spaceship <= y_obj:
        move_down = Move()
        move_down.down = True
        # while objects are not horizontally aligned
        while not (coord_tmp_spaceship[1] >= coord_tmp_obj[1]):
            counter_y += 1
            coord_tmp_spaceship[1] += obj1_tmp.get_fx_fy(move_down)[1]
            coord_tmp_obj[1] += vy_obj
            coord_tmp_spaceship[0] += obj1_tmp.get_fx_fy(move_down)[0]
            coord_tmp_obj[0] += vx_obj

        if (
                coord_tmp_spaceship[0] + threshold > coord_tmp_obj[0]
                and is_in_conflict(obj1_tmp, GameConfig.BOT_THRESHOLD, obj2_tmp)
        ):
            return coord_tmp_spaceship  # Coordinates of potential impact
        else:
            return 0

    # If the player spaceship is under the object
    if y_spaceship > y_obj:
        move_up = Move()
        move_up.up = True
        # while objects are not horizontally aligned
        while not (coord_tmp_spaceship[1] < coord_tmp_obj[1]):
            counter_y += 1
            coord_tmp_spaceship[1] += obj1_tmp.get_fx_fy(move_up)[1]
            coord_tmp_obj[1] += vy_obj
            coord_tmp_spaceship[0] += obj1_tmp.get_fx_fy(move_up)[0]
            coord_tmp_obj[0] += vx_obj

        if (
                coord_tmp_spaceship[0] + threshold > coord_tmp_obj[0]
                and is_in_conflict(obj1_tmp, GameConfig.BOT_THRESHOLD, obj2_tmp)
        ):
            return coord_tmp_spaceship
        else:
            return 0


class Bot(PlayerSpaceship):

    # Detecting an immediate danger from above y-axis
    def near_dangerous_object_upside(self, list_enemies_sorted):
        if len(list_enemies_sorted) == 0:
            return False
        for enemy in list_enemies_sorted:
            return (
                    self.rect.centery >= enemy.rect.centery >= self.rect.topright[1] + GameConfig.PLAYER_SPACESHIP_H
                    and (self.rect.left + GameConfig.PLAYER_SPACESHIP_W + GameConfig.BOT_THRESHOLD) >= enemy.rect.left
            )

    # Detecting an immediate danger from below y-axis
    def near_dangerous_object_downside(self, list_enemies_sorted):
        if len(list_enemies_sorted) == 0:
            return False
        for enemy in list_enemies_sorted:
            return (
                    self.rect.centery <= enemy.rect.centery <= self.rect.bottomright[1] - GameConfig.PLAYER_SPACESHIP_H
                    and (self.rect.left + GameConfig.PLAYER_SPACESHIP_W + GameConfig.BOT_THRESHOLD) >= enemy.rect.left
            )

    # Detecting objects above y-axis
    def get_objects_upside(self, list_danger, seuil):
        up_side = []
        for danger in list_danger:
            if danger.rect.center[1] <= self.rect.center[1] and self.rect.center[0] + seuil < danger.rect.center[0]:
                up_side.append(danger)
        return up_side

    # Detecting objects below y-axis
    def get_objects_downside(self, list_danger, seuil):
        down_side = []
        for danger in list_danger:
            if danger.rect.center[1] >= self.rect.center[1] and self.rect.center[0] + seuil < danger.rect.center[0]:
                down_side.append(danger)
        return down_side

    # Defines a new move to iterate of
    def define_new_tick_move(self, move, ticks):
        if self.move_cooldown == 0 and self.move_ticking is None:
            self.move_cooldown = ticks
            self.move_ticking = move

    # Defines if there is a move being iterated
    def is_move_ticking(self):
        if self.move_cooldown == 0:
            self.move_ticking = None
            return False
        else:
            self.move_cooldown -= 1
            return True

    @staticmethod
    # Return the list of ennemies present in game_state
    def get_list_enemies(game_state): return game_state.enemy_spaceships + game_state.asteroids

    @staticmethod
    # Sort by priority order according to proximity with player spaceship
    def sort_by_priority(enemies_list):
        a_list = list(enemies_list)
        a_list.sort(key=lambda x: x.rect.left)
        return a_list

    # Determines if the next move risks a collision
    def will_collide_next(self, game_state, next_move):
        objects = self.sort_by_priority(self.get_list_enemies(game_state))
        objects.pop(0)
        if next_move.up:
            return self.near_dangerous_object_upside(self.get_objects_upside(objects, GameConfig.BOT_THRESHOLD))
        if next_move.down:
            return self.near_dangerous_object_downside(self.get_objects_downside(objects, GameConfig.BOT_THRESHOLD))

    # Allows to find a path for positioning in front of spaceship
    def get_aggressive_path(self, game_state):
        moves_return = [Move()]
        list_enemies = self.get_list_enemies(game_state)
        dist_enemies = []
        for enemy in list_enemies:
            dist_enemies.append(get_distance_between_to_object(self, enemy))
        int_ppt = dist_enemies.index(min(dist_enemies))
        target = list_enemies[int_ppt]
        vaisseau_test = PlayerSpaceship(self.rect.x, self.rect.y)
        y_target = target.rect.centery
        y_vaisseau = vaisseau_test.rect.centery
        move_haut = Move()
        move_bas = Move()
        move_haut.up = True
        move_bas.down = True
        while not (y_target - 5 <= y_vaisseau <= y_target + 5):
            if y_target > y_vaisseau:
                next_move = move_bas
            else:
                next_move = move_haut
            fx, fy = vaisseau_test.get_fx_fy(next_move)
            y_vaisseau += fy
            y_target += target.vy
            moves_return.append(next_move)
        move_shoot = Move()
        move_shoot.shoot = True
        moves_return.append(move_shoot)
        return moves_return

    # Determines the move according to bot state
    def move_from_state(self, game_state):
        valid_moves = []

        moves_to_investigate = [Move(), Move(), Move(), Move()]
        moves_to_investigate[0].up = True
        moves_to_investigate[1].down = True
        moves_to_investigate[2].left = True
        moves_to_investigate[3].right = True

        if self.state == 1:
            for i in range(0, 2):
                if not self.will_collide_next(game_state, moves_to_investigate[i]):
                    valid_moves.append(moves_to_investigate[i])
            shuffle(valid_moves)
            if len(valid_moves) > 0:
                for i in range(0, GameConfig.BOT_MOVE_COOLDOWN):
                    self.move_stack.append(valid_moves[0])

        if self.state == 2:
            path = self.get_aggressive_path(game_state)
            for i in range(0, len(path)):
                self.move_stack.append(path[i])
        if len(self.move_stack) > 0:
            tmp = self.move_stack[0]
            self.move_stack.pop(0)
            return tmp

        return Move()

    # Update the state of the bot
    def update_state(self, coord_impact):
        if self.state_0_it == GameConfig.SHOT_COOLDOWN and not self.state == 1:
            self.state_0_it = 0
            self.state = 2

        elif len(coord_impact) == 0 and self.state == 0:
            self.state_0_it += 1

        elif len(coord_impact) > 0 and not self.state == 2:
            self.state_0_it = 0
            self.state = 1

        elif len(coord_impact) == 0:
            self.state = 0

    def get_next_move_ia(self, game_state):
        list_enemies = self.get_list_enemies(game_state)
        list_enemies_sorted = self.sort_by_priority(list_enemies)
        list_danger = []
        coord_impact = []
        if len(self.move_stack) != 0:
            next_move = self.move_stack[0]
            self.move_stack.pop(0)
            if next_move.up and self.near_dangerous_object_upside(
                    self.get_objects_upside(list_enemies_sorted, GameConfig.BOT_THRESHOLD)):
                next_move.up = False
            if next_move.down and self.near_dangerous_object_downside(
                    self.get_objects_downside(list_enemies_sorted, GameConfig.BOT_THRESHOLD)):
                next_move.down = False
            return next_move
        for enemy in list_enemies_sorted:
            if is_in_conflict(self, GameConfig.BOT_THRESHOLD, enemy):
                list_danger.append(enemy)
            elif self.near_dangerous_object_upside([enemy]):
                list_danger.append(enemy)
            elif self.near_dangerous_object_downside([enemy]):
                list_danger.append(enemy)
        for danger in list_danger:
            coord_impact.append(get_intersection_with_bot(self, danger, GameConfig.BOT_THRESHOLD))
        self.update_state(coord_impact)
        if len(self.move_stack) == 0:
            next_move = self.move_from_state(game_state)
        else:
            next_move = self.move_stack[0]
            self.move_stack.pop(0)
        return next_move

    # Update the state of the bot for the next game loop
    def advance_state(self, next_move, game_state):
        next_move = self.get_next_move_ia(game_state)
        self.vx, self.vy = self.get_fx_fy(next_move)
        self.shoot_action(next_move)
        self.rect = self.rect.move(self.vx, self.vy)
