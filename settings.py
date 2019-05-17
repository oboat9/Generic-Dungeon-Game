import pygame as pg
import random
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
CYAN = (0, 255, 255)

# Main Settings
WIDTH = 1280
HEIGHT = 720
FPS = 60

TITLE = "Generic Dungeon Game"
BGCOLOR = BROWN

NUMBEROFLEVELS = 2

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Wall Settings
WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_IMG = "manBlue_gun.png"
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(30, 10)

# Gun Settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 300
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10
GUN_AMMO = 12
RELOAD_TIME = 3000
MAX_GUN_MAGS = 6

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [150, 175, 200]
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 50
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png','whitePuff18.png']
FLASH_DURATION = 40

SPLAT = 'splat green.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png', 'ammo': 'ammo.png'}

HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.2

# Sounds
PLAYER_HIT_SOUNDS = ['playerhit.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']
EFFECTS_SOUNDS = {'health_up': 'health_pack.wav'}