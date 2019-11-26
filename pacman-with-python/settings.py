from pygame.math import Vector2 as vec
import random

# screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28

# colour settings
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)

# font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'

# player settings
# PLAYER_START_POS = vec(2, 2)

# mob settings

PLAYER1_START_POS = vec(1,1)
PLAYER2_START_POS = vec(26,29)

coin1_y = random.randint(10,20)
coin2_y = random.randint(10,20)
coin3_x = random.randint(13,14)
coin4_x = random.randint(13,14)
SUPER_COIN_1 = vec(6,coin1_y)
SUPER_COIN_2 = vec(21,coin2_y)
SUPER_COIN_3 = vec(coin3_x,11)
SUPER_COIN_4 = vec(coin4_x,17)
