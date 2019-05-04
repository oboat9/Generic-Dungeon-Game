# Generic Dungeon Game
# By Owen Stevenson
# started April 25th, 2019
# completed --

import sys
from os import path

# Main File
import pygame as pg

from settings import *
from sprites import *
from tilemap import *



class Game:
    # runs first
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))#, pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(1, 100)
        self.load_data()
        pg.mixer.init()

    # loads all the game files into pygame memory
    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, "map_folder")
        img_folder = path.join(game_folder, "img")
        snd_Folder = path.join(game_folder, "snd")
        snd_Music_Folder = path.join(snd_Folder,"Music")

        self.map = Map(path.join(map_folder, "map3.txt"))
        self.player_image = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        pg.mixer.music.load("snd/Music/Menu/mainmenu.wav")

    def new(self):
        # start the music
        pg.mixer.music.play(-1)
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        # turns the map text file into an actual game map
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        
        self.camera = Camera(self.map.width, self.map.height)

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

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)
    
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
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #drawing player hitbox for debug
            ##pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
        
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
        #this part below is for window resizing (may or may not add) (hidden)
            """
            if event.type == pg.VIDEORESIZE:
            # There's some code to add back window content here.
                surface = pg.display.set_mode((event.w, event.h),pg.RESIZABLE)
                HEIGHT = event.h
                WIDTH = event.w
            """    
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                
    # not used currently
    def show_start_screen(self):
        pass
    # not used currently
    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
