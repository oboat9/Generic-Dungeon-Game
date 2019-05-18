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
import random

current_Level = 'level1.tmx'

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
    pg.draw.rect(surf, BLACK, outline_rect, 2)

class Game:
    # runs first
    def __init__(self):
        #pg.mixer.pre_init(44100, -16, 1, 4069)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(1, 100)
        self.load_data(current_Level)
        pg.mixer.init()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        

    # loads all the game files into pygame memory
    def load_data(self, current_Level='level1.tmx'):
        map_folder = 'maps'
        img_folder = 'img'
        snd_Folder = 'snd'
        music_folder = 'music'
        
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.current_Level = current_Level
        self.map = TiledMap(path.join('maps', self.current_Level))

        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_image = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()

        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))

        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64,64))

        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        
        pg.mixer.music.load(path.join(snd_Folder,'mainmenu.wav'))
        self.player_die_snd = pg.mixer.Sound(path.join(snd_Folder,'Player Dying.wav'))
        self.zombie_die_snd = pg.mixer.Sound(path.join(snd_Folder,'ZombieDying.wav'))
        self.gun_reload_snd = pg.mixer.Sound(path.join(snd_Folder,'gun reload.wav'))
        self.no_ammo_reload = pg.mixer.Sound(path.join(snd_Folder,'no more reload.wav'))
        self.empty_mag = pg.mixer.Sound(path.join(snd_Folder,'no ammo.wav'))
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()


        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_Folder, EFFECTS_SOUNDS[type]))

        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for snd in WEAPON_SOUNDS_GUN:
            self.weapon_sounds['gun'].append(pg.mixer.Sound(path.join(snd_Folder,snd)))

        #self.zombie_moan_sounds = []
        #for snd in ZOMBIE_MOAN_SOUNDS:
            #self.zombie_moan_sounds.append(pg.mixer.Sound(path.join(snd_Folder,snd)))
            
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_Folder, snd)))

        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_Folder, snd)))

    def new(self):
        
        # start the music
        pg.mixer.music.set_volume(0.75)
        pg.mixer.music.play(-1)
        
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
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
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height /2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['ammo']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.mobs_left = len(self.mobs)
        #self.effects_sounds['level_start'].play()

    def run(self):
        # game loop -- set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
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
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
                # player hits healthpack
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'ammo' and self.player.remaining_magazines < MAX_GUN_MAGS:
                self.player.add_ammo(MAX_GUN_MAGS)
                self.effects_sounds['ammo_pickup'].play()
                hit.kill()
        #print(self.mobs_left)
        #print(len(self.mobs))
        #print(self.player.pos)

        # when the player gets hit
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
                # makes the sound play whatever percentage of the hits you set it to
            if random.random() < 1:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                channel=self.player_die_snd.play()
                self.playing = False
                pg.mixer.music.stop()
                time.sleep(1)
                RunGame()
            
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)
        
        if self.player.rect.left > self.map_rect.right-TILESIZE and len(self.mobs) == 0:
            self.playing = False
        if self.player.rect.left > self.map_rect.right-(TILESIZE*7) and self.player.rect.top > self.map_rect.bottom-(TILESIZE*7) and len(self.mobs) == 0:
            self.playing = False
        
    
    #draws the grid (not in use currently)
    def draw_grid(self):

        # vertical lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
         # horizontal lines
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
     # draws everything including the final 'pg.display.flip()' command
    def draw(self):
        pg.display.set_caption('fps: '+'{:.2f}'.format(self.clock.get_fps())+' -- Zombies Remaning: '+str(len(self.mobs))+' - Ammo : '+str(self.player.remaining_ammo)+' - Clips : '+str(self.player.remaining_magazines))
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
        if self.paused:
            self.screen.blit(self.dim_screen,(0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")

        #self.draw_text(str(self.mobs_left), self.title_font, 105, BLACK, WIDTH/2, HEIGHT/2, align="sw")

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
                if event.key == pg.K_p:
                    self.paused = not self.paused
                    if self.paused:
                        pg.key.set_repeat()
                        pg.mixer.music.pause()
                    elif not self.paused:
                        pg.key.set_repeat(1, 100)
                        pg.mixer.music.unpause()

                
    # not used currently
    def show_start_screen(self):
        self.current_Level = 'level1.tmx'
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
        current_Level = 'level' + str(levelnum) + '.tmx'

        if levelnum > NUMBEROFLEVELS:
            levelnum = 0

g = Game()
current_Level = 'level1.tmx'
levelnum = 1
g.show_start_screen()