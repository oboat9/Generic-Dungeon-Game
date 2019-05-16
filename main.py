# Generic Dungeon Game
# By Owen Stevenson
# started April 25th, 2019
# completed --

import sys
from os import path

# Main File
import pygame as pg
import pytmx
import time

from settings import *
from sprites import *
from tilemap import *

current_Level = "level1.tmx"

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    # runs first
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(1, 100)
        self.load_data(current_Level)
        pg.mixer.init()
        

    # loads all the game files into pygame memory
    def load_data(self, current_Level="level1.tmx"):
        map_folder = "maps"
        img_folder = "img"
        snd_Folder = "snd"

        self.current_Level = current_Level
        self.map = TiledMap(path.join("maps", self.current_Level))

        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_image = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        
        
        pg.mixer.music.load(path.join(snd_Folder,"mainmenu.wav"))
        self.player_die_snd = pg.mixer.Sound(path.join(snd_Folder,"Player Dying.wav"))

    def new(self):
        
        # start the music
        
        pg.mixer.music.play(-1)
        
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        # turns the map text file into an actual game map
            #for row, tiles in enumerate(self.map.data):
            #    for col, tile in enumerate(tiles):
            #        if tile == '1':
            #            Wall(self, col, row)
            #        if tile == 'P':
            #            self.player = Player(self, col, row)
            #        if tile == 'M':
            #            Mob(self, col, row)
        
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "zombie":
                Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        # game loop -- set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    #quits the game
    def quit(self):
        pg.quit()
        exit(0)

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        print(len(self.mobs))

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                channel=self.player_die_snd.play()
                self.playing = False
                RunGame()
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)
        
        if self.player.rect.left > self.map_rect.right-TILESIZE and len(self.mobs) == 0:
            self.playing = False
    
    #draws the grid (not in use currently)
    def draw_grid(self):

        # vertical lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
         # horizontal lines
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
     # draws everything including the final "pg.display.flip()" command
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 4)
            if self.draw_debug:
                for wall in self.walls:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 4)


            ##pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
        
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                
    # not used currently
    def show_start_screen(self):
        self.current_Level = "level1.tmx"
        RunGame()
    # not used currently
    def show_go_screen(self):
        pg.mixer.music.stop()


# create the game object
def RunGame():
    global current_Level, levelnum
    while True:
        #current_Level = g.current_Level
        g.load_data(current_Level)
        g.new()
        g.run()
        levelnum += 1
        current_Level = "level" + str(levelnum) + ".tmx"

        if levelnum > NUMBEROFLEVELS:
            levelnum = 1

g = Game()
current_Level = "level1.tmx"
levelnum = 1
g.show_start_screen()