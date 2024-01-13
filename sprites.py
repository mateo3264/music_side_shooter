import pygame as pg
from settings import *
import random
from midipatternspkg import patterns
from pygame import midi 
import csv
import datetime



vec = pg.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        return image

def hit(element, group, func):
    hits = pg.sprite.spritecollide(element, group, True, collide_hit_rect)

    if hits:
        func(hits[0])

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
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.hit_rect = self.rect.copy()
        
        self.hit_rect.width -= 10
        self.hit_rect.height =  int(.1 * self.hit_rect.height)


        self.rect.topleft = self.pos

        self.vy = 7
        self.vx = 7

        self.n_bullets = 100

        

        pattern_player_mov = NOTES
        pattern_player_mov = [note + 6 * 2 for note in pattern_player_mov]
        pattern_bullet = [note + 0 * 2 for note in pattern_player_mov]
        self.pattern_player_mov = patterns.PatternChecker2(pattern_player_mov)
        self.pattern_bullet = patterns.PatternChecker2(pattern_bullet)


        
    
    def get_pressed_keys(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP]:
            self.pos.y -= self.vy
        if keys[pg.K_DOWN]:
            self.pos.y += self.vy
            
    def if_hit(self, mob):
         
        self.game.n_lifes -= 1
        self.game.playing = False
        print('self.n_lifes')
        print(self.game.n_lifes)
        if self.game.n_lifes == 0:
            self.game.running = False
        self.kill()       

    def update(self):
        self.get_pressed_keys()  
        if self.game.midi_input.poll():
            midi_events = self.game.midi_input.read(1)
            midi2events = midi.midis2events(midi_events, 1)
            idx = self.pattern_player_mov.check_pattern(midi2events, type='one-note')      
            idx_bullet = self.pattern_bullet.check_pattern(midi2events, type='one-note')
            
            if isinstance(idx, int):
                print(idx)
                self.pos.y = 2 * HEIGHT // 3  - int(idx / 30 * HEIGHT)
                print(self.pos.y)
            
            if isinstance(idx_bullet, int):
                if self.n_bullets > 0:
                    Bullet(self.game, self.pos.x, 2 * HEIGHT // 3  - int(idx_bullet / 30 * HEIGHT))
                    self.n_bullets -= 1

        self.rect.center = self.pos
        self.hit_rect = self.rect.copy()
        
        self.hit_rect.width -= 10
        self.hit_rect.height = int(.1 * self.hit_rect.height)
        self.hit_rect.y += self.rect.height // 2 - self.hit_rect.height // 2

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
        self.hit_rect = self.rect.copy()
    
    def if_hits(self, mob):
        
        self.game.n_mobs_dodged += 1
        self.game.score += 1
        self.cur_time = pg.time.get_ticks()

        latency = self.cur_time - mob.time_when_appears
        with open('latency_performance.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow([str(datetime.datetime.now()), mob.note, latency])
        self.kill()

    def update(self):
        self.pos.x += 20

        self.rect.center = self.pos

        self.hit_rect = self.rect.copy()

        if self.rect.left > WIDTH:
            self.kill()

        hit(self, self.game.mobs, self.if_hits)



class Mob(pg.sprite.Sprite):
    def __init__(self, game, x=None, velx=1):
        self.groups = game.all_sprites, game.mobs

        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        side = TILESIZE // 3
        self.orig_image = pg.image.load('meteorBrown_tiny1.png').convert()#pg.Surface((side, side))
        self.image = self.orig_image.copy()
        #self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()
        

        self.y_positions = [2 * HEIGHT // 3  - int(note / 30 * HEIGHT) for note in range(12)]
        print('self.y_positions')
        print(self.y_positions)
        self.n_possible_pos = 2
        
        if x is None:
            x = random.randrange(WIDTH, WIDTH + side // 3)
        y_pos_idx = random.randrange(len(self.y_positions))
        y_pos = self.y_positions[y_pos_idx]
        self.pos = vec(x, y_pos)

        self.note = idxs_to_labels[y_pos_idx]

        self.rect.center = self.pos

        self.vx = velx
        self.rot_angle = 0

        self.time_when_appears = None

        self.appear = True
    
    def update(self):
        self.rot_angle += 10
        self.image = pg.transform.rotate(self.orig_image, self.rot_angle)
        self.rect = self.image.get_rect()
        self.pos.x -= self.vx

        self.rect.center = self.pos

        self.hit_rect = self.rect.copy()
        
        if self.rect.left < WIDTH:
            if self.appear:
                self.time_when_appears = pg.time.get_ticks()
                self.appear = not self.appear
        if self.rect.right < 0:
            self.game.n_mobs_dodged += 1
            self.kill()
            

