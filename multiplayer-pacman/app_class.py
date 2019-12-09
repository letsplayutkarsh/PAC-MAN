import pygame
import sys
import copy

from settings import *
from player_class import *
from enemy_class_1 import *
from enemy_class_2 import *

pygame.init()

vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MULTIPLAYER PAC-MAN")
        icon = pygame.image.load('pacman.jpg')
        pygame.display.set_icon(icon)

        # self.pacman_eat = pygame.mixer.music.load('pac-man_eat_fruit.wav')
        self.background_music = pygame.mixer.music.load('pac_man.mp3')


        self.player_1_mortal = True
        self.player_2_mortal = True
        self.player_1_mortal_dummy = True
        self.player_2_mortal_dummy = True

        self.clock = pygame.time.Clock()

        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.super_coin_list = []

        self.enemies_1 = []
        self.enemies_2 = []
        self.e_pos_1 = []
        self.e_pos_2 = []

        self.load()

        self.player = Player(self, PLAYER1_START_POS, PLAYER2_START_POS)
        self.make_enemies_1()
        self.make_enemies_2()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()

            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()


            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()

            elif self.state == 'instrusction':
                self.instrusction_events()
                self.instrusction_update()
                self.instrusction_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################ HELPER FUNCTIONS ##################################

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        pygame.mixer.music.play(-1)
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(
            self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "S":
                        self.super_coin_list.append(vec(xidx, yidx))
                    elif char in ["2", "4"]:
                        self.e_pos_1.append([xidx, yidx])
                    elif char in ["3", "5"]:
                        self.e_pos_2.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies_1(self):
        for idx, pos in enumerate(self.e_pos_1):
            self.enemies_1.append(Enemy_1(self, vec(pos), idx))

    def make_enemies_2(self):
        for idx, pos in enumerate(self.e_pos_2):
            self.enemies_2.append(Enemy_2(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))


    def reset(self):
        self.player.lives_1 = 3
        self.player.lives_2 = 3
        self.player.current_score_1 = 0
        self.player.current_score_2 = 0
        self.player.grid1_pos = vec(1, 1)
        self.player.grid2_pos = vec(26, 29)

        self.player.pix_pos1 = self.player.get_pix_pos1()
        self.player.pix_pos2 = self.player.get_pix_pos2()

        self.player.direction1 *= 0
        self.player.direction2 *= 0

        for enemy in self.enemies_1:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
            
        for enemy in self.enemies_2:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.super_coin_list = []
        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
                    elif char == "S":
                        self.super_coin_list.append(vec(xidx, yidx))

        self.state = "playing"


########################### INTRO FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.state = 'instrusction'




    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACEBAR TO START', self.screen, [
                       WIDTH // 2, HEIGHT // 2 + 20], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('MULTIPLAYER PAC-MAN', self.screen, [
                       WIDTH // 2, HEIGHT // 2 - 50], START_TEXT_SIZE + 15, (44, 167, 198), START_FONT, centered=True)

        self.draw_text('PUSH i FOR INSTRUCTIONS', self.screen, [
                       WIDTH // 2, HEIGHT // 2 + 70], START_TEXT_SIZE - 10, (44, 167, 198), START_FONT, centered=True)

        pygame.display.update()
########################### INSTRUCTION FUNCTIONS ##################################

    def instrusction_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def instrusction_update(self):
        pass

    def instrusction_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACEBAR TO START', self.screen, [
                       WIDTH // 2, HEIGHT // 2 + 230], START_TEXT_SIZE - 5, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('MULTIPLAYER PAC-MAN INSTRUCTIONS', self.screen, [
                       WIDTH // 2, HEIGHT // 2 - 230], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)

        pygame.draw.circle(self.screen, (250, 225, 0), [
                           100, 180], self.cell_width // 2 - 3)
        self.draw_text('Player1 ', self.screen, [
                       130, 170], START_TEXT_SIZE, (250, 225, 0), START_FONT, centered=False)

        self.draw_text('W - move up', self.screen,
                       [100, 220], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)
        self.draw_text('S - move down', self.screen,
                       [100, 250], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)
        self.draw_text('D - move right', self.screen,
                       [100, 280], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)
        self.draw_text('A - move left', self.screen,
                       [100, 310], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)

        pygame.draw.circle(self.screen, (255, 0, 0), [
                           370, 180], self.cell_width // 2 - 3)
        self.draw_text('Player2 ', self.screen, [
                       400, 170], START_TEXT_SIZE, (255, 0, 0), START_FONT, centered=False)

        self.draw_text('up arrow - move up', self.screen,
                       [340, 220], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)
        self.draw_text('down arrow - move down', self.screen,
                       [340, 250], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)
        self.draw_text('right arrow - move right', self.screen,
                       [340, 280], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)
        self.draw_text('left arrow - move left', self.screen,
                       [340, 310], START_TEXT_SIZE - 8, (170, 132, 58), START_FONT, centered=False)

        self.draw_text('If player losses a life then 5 points will be deducted', self.screen, [
                       WIDTH // 2, 420], START_TEXT_SIZE - 8, (76, 151, 212), START_FONT, centered=True)
        self.draw_text('and will move to its original position but other player', self.screen, [
                       WIDTH // 2, 450], START_TEXT_SIZE - 8, (76, 151, 212), START_FONT, centered=True)
        self.draw_text('will retain its current position but ghosts will go to their nests', self.screen, [
                       WIDTH // 2, 480], START_TEXT_SIZE - 8, (76, 151, 212), START_FONT, centered=True)

        pygame.display.update()
########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.move1(vec(-1, 0))
                if event.key == pygame.K_d:
                    self.player.move1(vec(1, 0))
                if event.key == pygame.K_w:
                    self.player.move1(vec(0, -1))
                if event.key == pygame.K_s:
                    self.player.move1(vec(0, 1))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move2(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move2(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move2(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move2(vec(0, 1))

            self.state = "playing"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def playing_update(self):

        self.player.update()

        for enemy in self.enemies_1:
            enemy.update()

        for enemy in self.enemies_2:
            enemy.update()

        for enemy in self.enemies_1:
            if enemy.grid_pos == self.player.grid1_pos:
                self.remove_life_1()

            if enemy.grid_pos == self.player.grid2_pos:
                self.remove_life_2()


        for enemy in self.enemies_2:
            if enemy.grid_pos == self.player.grid1_pos:
                self.remove_life_1()


            if enemy.grid_pos == self.player.grid2_pos:
                self.remove_life_2()



    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(
            self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.draw_super_coins()

        # self.draw_grid()

        # self.draw_grid()
        self.draw_text('PLAYER1-SCORE: {}'.format(self.player.current_score_1),
                       self.screen, [60, 6], 24, WHITE, START_FONT)
        self.draw_text('PLAYER2-SCORE: {}'.format(self.player.current_score_2),
                       self.screen, [385, 6], 24, WHITE, START_FONT)
        self.player.draw()

        for enemy in self.enemies_1:
            enemy.draw()
        for enemy in self.enemies_2:
            enemy.draw()

        pygame.display.update()

    def remove_life_1(self):

        if(self.player_1_mortal):
            self.player.lives_1 -= 1
            self.player.current_score_1 -= 10

            if self.player.lives_1 == 0 :
                self.state = "game over"
            else:
                self.player.grid1_pos = vec(1, 1)
                self.player.pix_pos1 = self.player.get_pix_pos1()
                self.player.direction1 *= 0

                for enemy in self.enemies_1:
                    enemy.grid_pos = vec(enemy.starting_pos)
                    enemy.pix_pos = enemy.get_pix_pos()
                    enemy.direction *= 0
                for enemy in self.enemies_2:
                    enemy.grid_pos = vec(enemy.starting_pos)
                    enemy.pix_pos = enemy.get_pix_pos()
                    enemy.direction *= 0

    def remove_life_2(self):

        if(self.player_2_mortal):
            self.player.lives_2 -= 1
            self.player.current_score_2 -= 10


            if self.player.lives_2 == 0 :
                self.state = "game over"
            else:
                self.player.grid2_pos = vec(26, 29)
                self.player.pix_pos2 = self.player.get_pix_pos2()
                self.player.direction2 *= 0

                for enemy in self.enemies_1:
                    enemy.grid_pos = vec(enemy.starting_pos)
                    enemy.pix_pos = enemy.get_pix_pos()
                    enemy.direction *= 0
                for enemy in self.enemies_2:
                    enemy.grid_pos = vec(enemy.starting_pos)
                    enemy.pix_pos = enemy.get_pix_pos()
                    enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def draw_super_coins(self):
        for coin in self.super_coin_list:
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 7)
########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass


    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "PRESS THE ESCAPE BUTTON TO QUIT"
        again_text = "PRESS SPACEBAR TO PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [
                       WIDTH // 2, 100],  52, RED, "arial", centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH // 2, HEIGHT // 2 + 100],  30, (190, 190, 190), "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH // 2, HEIGHT // 1.5 + 60],  30, (190, 190, 190), "arial", centered=True)

        if self.player.current_score_1 > self.player.current_score_2:
            self.draw_text("PLAYER-1 WON", self.screen, [
                           WIDTH // 2, HEIGHT // 2 - 20],  40, (10, 147, 233), "arial", centered=True)
        elif self.player.current_score_1 < self.player.current_score_2:
            self.draw_text("PLAYER-2 WON", self.screen, [
                           WIDTH // 2, HEIGHT // 2 - 20],  40, (10, 147, 233), "arial", centered=True)
        else:
            self.draw_text("IT'S A TIE", self.screen, [
                           WIDTH // 2, HEIGHT // 2 - 20],  40, (10, 147, 233), "arial", centered=True)

        self.draw_text('PLAYER1-SCORE: {}'.format(self.player.current_score_1),
                       self.screen, [60, 200], 25, (197, 241, 145), START_FONT)
        self.draw_text('PLAYER2-SCORE: {}'.format(self.player.current_score_2),
                       self.screen, [360, 200], 25, (197, 241, 145), START_FONT)
        pygame.display.update()
