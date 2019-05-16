import pygame as pg
import pytmx
from random import uniform, choice

from settings import *
from tilemap import *
vec = pg.math.Vector2

 # collision dectection code that can be used with any sprite
def collide_with_walls(sprite, group, dir):

     # horizonal collisions
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

     # vertical collisions
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image
        self.rect = self.image.get_rect()
         # give the hitbox a seperate rectangle 
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH

     # gets the keypresses every tick
    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
         # rotating
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
         # forwards & backwards
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)



         # shooting bullets
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)

                 # kicks the player back when shooting
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)


    def update(self):
            # gets key updates
        self.get_keys()
            # rotates the player when the turning keys are pressed
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_image, self.rot)
            # updates the rectangle after turning
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x

            # horizontal collisions
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
            # vertical collisions
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
            # makes the bullets look more realistic by making slight bullet spread
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
            # helps with shooting interval when holding down button
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
            # kills the bullest when it hits a wall
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
            # kills bullet after [BULLET_LIFETIME]
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()

            # makes sure each mob has its own hitbox
        self.hit_rect = MOB_HIT_RECT.copy()

        self.hit_rect.center = self.rect.center

        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
            # rotates the mob
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)

            # gets the new rect after rotating
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

            # makes the mob chase the player
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
            # updates mob location to match the new rotation/location

        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # updates hitbox to match rectangle
        self.hit_rect.centerx = self.pos.x

            # horizontal collisions
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        
            # vertical collisions
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

            # when health less than zero kill the mob
        if self.health <= 0:
            self.kill()
    
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED

        width = int(self.rect.width * self.health/100)
        self.health_bar = pg.Rect(0,0, width, 7)

        if self.health < 100:
            pg.draw.rect(self.image, col, self.health_bar)  
        

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img

        #for making the walls plain rectangles without an image
            ##self.image = pg.Surface((TILESIZE, TILESIZE))
            ##self.image.fill(DARKRED)

        self.rect = self.image.get_rect()
            # sets the location
        self.x = x
        self.y = y
            # makes sure the walls are the same size as the [TILESIZE]
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = pg.Rect(x, y, w, h)
            # sets the location
        self.x = x
        self.y = y
            # makes sure the walls are the same size as the [TILESIZE]
        self.rect.x = x
        self.rect.y = y