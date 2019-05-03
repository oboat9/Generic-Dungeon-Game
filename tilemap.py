import pygame as pg

from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

 # makes the map .txt file into a game map
class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
    
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

 # makes the game follow the player around when you are moving past the threshold
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2) 
        y = -target.rect.centery + int(HEIGHT / 2)

         # limit scrolling to map size (so you don't see past the edge)
            # when you get near the edge of the map the camera stops following
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) #bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
        
