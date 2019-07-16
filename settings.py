from os import path

WIDTH = 480 #width of the game window
HEIGHT = 640 #height of the game window
CENTER = int(WIDTH/2)
FPS = 60 #frames per second that the game runs - action game to run quickly
REQUIRED_HITS = 200
ENEMY_NR_START = 8
LEVEL = 5
LEVEL_UP = 25
EARTH1 = 1
EARTH2 = 2
GUN_VOLUME = 0.2
EXPLOSION_VOLUME = 0.5
MUSIC_VOLUME = 0.3

PLAYER_SPEED = 5 # NOT set
ENEMY_SPEEDY_MAX_L1 = 5 # NOT set
ENEMY_SPEEDY_MAX_L2 = 7 # NOT set
ENEMY_SPEEDY_MAX_L3 = 9 # NOT set
ENEMY_SPEEDY_MAX_TO_FAST = 11 # NOT set
ENEMY_SPEEDY_MIN = 1 # NOT set
ENEMY_SPEEDY_MIN_2 = 3 # NOT set
BULLET_SPEED = 10 # NOT set
METEOR_MIN = 20 # NOT set
METEOR_MAX = 55 # NOT set

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

IMG_DIR = path.join(path.dirname(__file__), 'assets/img')
SOUND_DIR = path.join(path.dirname(__file__), 'assets/sounds')