# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg
import random
from settings import *
from sprites import *
from pygame import midi
import time
import csv

pg.init()
midi.init()


font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.n_lifes = 3

        

        try:
            self.midi_input = midi.Input(1)
            
        except:
            print('no piano')

        self.with_music = False

        if self.with_music:
            try:
                self.midi_out = midi.Output(0)
            except:
                print('no midi output')

        self.player_spritesheet = Spritesheet('player.png')
        #self.space_background_spritesheet = Spritesheet('sss.png')
        self.space_img1 = pg.image.load('background_1.png').convert_alpha()
        self.space_img1 = pg.transform.scale(self.space_img1, (WIDTH, HEIGHT))
        self.bg_imgs = [[self.space_img1, 0]]
        self.bg_imgs.append([self.space_img1, WIDTH])
        self.space_img1_rect = self.space_img1.get_rect()

        for i in range(2, 5):
            im = pg.image.load(f'background_{i}.png').convert_alpha()
            im = pg.transform.scale(im, (WIDTH, HEIGHT))
            self.bg_imgs.append([im, 0])
            self.bg_imgs.append([im, WIDTH])


        self.rhythm_pattern = [2, 1, 1]
        self.rhythm_idx = 0

        avg_latency_file = open('avg_latency.csv', 'r')
        reader = csv.reader(avg_latency_file)
        #header = next(reader)
        
        self.latency_avgs = [*reader][0]
        self.latency_avgs = [float(avg_latency) for avg_latency in self.latency_avgs]
        
        avg_latency_file.close()
        #self.last_time = time.time()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.score = 0

        self.mob_velx = 3

        self.n_mobs_dodged = 0

        self.change_mobs_vel = False
        self.change_mobs_vel_criteria = 3

        self.draw_debug = False
        
        for i in range(1):
            Mob(self, velx=self.mob_velx)
            #Mob(self)

        self.has_shot = False
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        self.sum_ms = 0
        while self.playing:
            self.sum_ms += self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        
        
        self.change_mobs_vel = False
        self.all_sprites.update()
        
        if self.sum_ms >= 1000 * self.rhythm_pattern[self.rhythm_idx]:
            self.sum_ms = 0
            self.rhythm_idx = (self.rhythm_idx + 1) % len(self.rhythm_pattern)#len(self.mobs) < 1:
            random_x = random.randrange(WIDTH, 2  * WIDTH)
            Mob(self, random_x, velx=self.mob_velx)
            
            
            
        
        # TODO: improve the gradual difficulty mechanism
        if self.change_mobs_vel_criteria == self.n_mobs_dodged:
            
                self.mob_velx += 1
                self.n_mobs_dodged = 0
            

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    
                    self.has_shot = True
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    
                    self.draw_debug = not self.draw_debug
            
        
    def draw_pentagram(self):
        for y in range(HEIGHT // 3, 2 * HEIGHT // 3, int(1 / 15 * HEIGHT)):
            
            pg.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))
    
    def draw_background(self):
        speed = 1
        for i, el in enumerate(self.bg_imgs):
            
            if i % 2 == 0:
                speed -= .2
            el[1] -= speed
            if el[1] <= -WIDTH:
                el[1] = WIDTH
            self.screen.blit(el[0], (el[1], 0))
    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)

        self.draw_pentagram()

        self.draw_background()

        bg = pg.Surface((WIDTH, HEIGHT))
        bg.set_alpha(180)
        bg.fill(BLACK)
        self.screen.blit(bg, (0, 0))
        #self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)
            if self.draw_debug:
                
                pg.draw.rect(self.screen, RED, sprite.hit_rect, 1)
            
        draw_text(self.screen, 'score: ' + str(self.score), 30, WIDTH - 50, 50)

        

        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()

with open('avg_latency.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(g.latency_avgs)