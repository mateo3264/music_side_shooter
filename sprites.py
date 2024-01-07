import pygame as pg
from settings import *
import random
vec = pg.math.Vector2


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        return image

def hit(element, group, func):
    hits = pg.sprite.spritecollide(element, group, True)

    if hits:
        func()

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = 3
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game

        
        self.pos = vec(TILESIZE, HEIGHT // 2 - TILESIZE // 2)

        self.image = self.game.player_spritesheet.get_image(0, 0, 64, 64)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (self.rect.width * 2, self.rect.height * 2))
        self.rect = self.image.get_rect()


        self.rect.topleft = self.pos

        self.vy = 7
        self.vx = 7

        
    
    def get_pressed_keys(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP]:
            self.pos.y -= self.vy
        if keys[pg.K_DOWN]:
            self.pos.y += self.vy
            
    def if_hit(self):
        self.kill()        

    def update(self):
        self.get_pressed_keys()        

        self.rect.center = self.pos

        if self.game.has_shot:
            self.game.has_shot = False
            Bullet(self.game, self.pos.x, self.pos.y)

        hit(self, self.game.mobs, self.if_hit)



class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)


        self.game = game

        self.pos = vec(x, y)

        self.image = pg.Surface((8, 8))
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.rect.center = self.pos
    
    def if_hits(self):

        self.kill()

    def update(self):
        self.pos.x += 20

        self.rect.center = self.pos

        if self.rect.left > WIDTH:
            self.kill()

        hit(self, self.game.mobs, self.if_hits)



class Mob(pg.sprite.Sprite):
    def __init__(self, game, x=None):
        self.groups = game.all_sprites, game.mobs

        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.Surface((TILESIZE, TILESIZE))

        self.image.fill(BLUE)

        self.rect = self.image.get_rect()

        if x is None:
            x = random.randrange(WIDTH, 2 * WIDTH)
        
        self.pos = vec(x, random.randrange(0, HEIGHT - TILESIZE // 2))

        self.rect.topleft = self.pos

        self.vx = 8
    
    def update(self):
        self.pos.x -= self.vx
        self.rect.topleft = self.pos

        if self.rect.right < 0:
            self.kill()
            

