import pygame as pg
vec = pg.math.Vector2

# preset colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255,0,0)
DARKRED = (128, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (106, 55, 5)

# Main Settings
WIDTH = 1600   # should be divisible by 32 but not required
HEIGHT = 900  # should be divisible by 32 but not required
FPS = 60

TITLE = "Generic Dungeon Game"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Wall Settings
WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_SPEED = 300
PLAYER_IMG = "manBlue_gun.png"
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(30, 10)

# Gun Settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 100