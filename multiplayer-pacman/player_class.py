import pygame
from settings import *
vec = pygame.math.Vector2

class Player:
    def __init__(self, app, pos1,pos2):
        self.app = app

        self.grid1_pos = pos1
        self.grid2_pos = pos2
        self.pix_pos1 = self.get_pix_pos1()
        self.pix_pos2 = self.get_pix_pos2()

        self.direction1 = vec(1, 0)
        self.direction2 = vec(-1, 0)
        self.stored_direction1 = None
        self.stored_direction2 = None

        self.able_to_move_1 = True
        self.able_to_move_2 = True
        self.current_score_1 = 0
        self.current_score_2 = 0
        self.speed = 2

        self.lives_1 = 3
        self.lives_2 = 3

    def update(self):

        if self.able_to_move_1:
            self.pix_pos1 += self.direction1 * self.speed

        if self.able_to_move_2:
            self.pix_pos2 += self.direction2 * self.speed

        if self.time_to_move_1():
            if self.stored_direction1 != None:
                self.direction1 = self.stored_direction1
            self.able_to_move_1 = self.can_move_1()

        if self.time_to_move_2():
            if self.stored_direction2 != None:
                self.direction2 = self.stored_direction2
            self.able_to_move_2 = self.can_move_2()
        # Setting grid position in reference to pix pos

        self.grid1_pos[0] = (self.pix_pos1[0] - TOP_BOTTOM_BUFFER +
                             self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid1_pos[1] = (self.pix_pos1[1] - TOP_BOTTOM_BUFFER +
                             self.app.cell_height // 2) // self.app.cell_height + 1
        self.grid2_pos[0] = (self.pix_pos2[0] - TOP_BOTTOM_BUFFER +
                             self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid2_pos[1] = (self.pix_pos2[1] - TOP_BOTTOM_BUFFER +
                             self.app.cell_height // 2) // self.app.cell_height + 1

        if self.on_coin1():
            self.eat_coin1()

        if self.on_supercoin1():
            self.eat_supercoin1()

        if self.on_coin2():
            self.eat_coin2()

        if self.on_supercoin2():
            self.eat_supercoin2()

    def draw(self):
        pygame.draw.circle(self.app.screen,(250,225,0),(int(self.pix_pos1.x),int(self.pix_pos1.y)),self.app.cell_width//2-2)
        pygame.draw.circle(self.app.screen,(255,0,0),(int(self.pix_pos2.x),int(self.pix_pos2.y)),self.app.cell_width//2-2)


        # Drawing player lives
        for x in range(self.lives_1):
            pygame.draw.circle(self.app.screen, (250,225,0),
                               (50 + 20 * x, HEIGHT - 15), 7)
        for x in range(self.lives_2):
            pygame.draw.circle(self.app.screen, (255,0,0),
                               (520 + 20 * x, HEIGHT - 15), 7)


    def on_coin1(self):
        if self.grid1_pos in self.app.coins:
            if int(self.pix_pos1.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction1 == vec(1, 0) or self.direction1 == vec(-1, 0):
                    return True
            if int(self.pix_pos1.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction1 == vec(0, 1) or self.direction1 == vec(0, -1):
                    return True
        return False

    def on_supercoin1(self):
        if self.grid1_pos in self.app.super_coin_list:
            if int(self.pix_pos1.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction1 == vec(1, 0) or self.direction1 == vec(-1, 0):
                    return True
            if int(self.pix_pos1.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction1 == vec(0, 1) or self.direction1 == vec(0, -1):
                    return True
        return False


    def on_coin2(self):
        if self.grid2_pos in self.app.coins:
            if int(self.pix_pos2.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction2 == vec(1, 0) or self.direction2 == vec(-1, 0):
                    return True
            if int(self.pix_pos2.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction2 == vec(0, 1) or self.direction2 == vec(0, -1):
                    return True
        return False

    def on_supercoin2(self):
        if self.grid2_pos in self.app.super_coin_list:
            if int(self.pix_pos2.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction2 == vec(1, 0) or self.direction2 == vec(-1, 0):
                    return True
            if int(self.pix_pos2.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction2 == vec(0, 1) or self.direction2 == vec(0, -1):
                    return True
        return False


    def eat_coin1(self):
        self.app.coins.remove(self.grid1_pos)
        self.current_score_1+= 1

    def eat_coin2(self):
        self.app.coins.remove(self.grid2_pos)
        self.current_score_2+= 1

    def eat_supercoin1(self):
        self.app.super_coin_list.remove(self.grid1_pos)
        self.current_score_1+= 1
        for enemy in self.app.enemies_1:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

    def eat_supercoin2(self):
        self.app.super_coin_list.remove(self.grid2_pos)
        self.current_score_2+= 1
        for enemy in self.app.enemies_2:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0


    def move1(self,direction1):
        self.stored_direction1 = direction1
    def move2(self,direction2):
        self.stored_direction2 = direction2

    def get_pix_pos1(self):
        return vec(((self.grid1_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2),((self.grid1_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2))
    def get_pix_pos2(self):
        return vec(((self.grid2_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2),((self.grid2_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2))



    def time_to_move_1(self):

        if int(self.pix_pos1.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction1 == vec(1, 0) or self.direction1 == vec(-1, 0) or self.direction1 == vec(0, 0):
                return True
        if int(self.pix_pos1.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction1 == vec(0, 1) or self.direction1 == vec(0, -1) or self.direction1 == vec(0, 0):
                return True

    def time_to_move_2(self):
        if int(self.pix_pos2.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction2 == vec(1, 0) or self.direction2 == vec(-1, 0) or self.direction2 == vec(0, 0):
                return True
        if int(self.pix_pos2.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction2 == vec(0, 1) or self.direction2 == vec(0, -1) or self.direction2 == vec(0, 0):
                return True

    def can_move_1(self):
        for wall in self.app.walls:
            if vec(self.grid1_pos + self.direction1) == wall:
                return False
        return True

    def can_move_2(self):
        for wall in self.app.walls:
            if vec(self.grid2_pos + self.direction2) == wall:
                return False
        return True
