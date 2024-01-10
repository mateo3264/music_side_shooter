# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg
import random
from settings import *
from sprites import *
from pygame import midi

pg.init()
midi.init()

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
        self.player_spritesheet = Spritesheet('player.png')

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.mob_velx = 5

        self.n_mobs_dodged = 0

        self.try_augment_mob_velx = False
        
        for i in range(1):
            Mob(self, velx=self.mob_velx)
            #Mob(self)

        self.has_shot = False
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        if len(self.mobs) < 1:
            random_x = random.randrange(WIDTH, 2  * WIDTH)
            Mob(self, random_x, velx=self.mob_velx)
            
            #Mob(self, random_x)
        
        # TODO: improve the gradual difficulty mechanism
        # if self.n_mobs_dodged % 3 == 0 and self.n_mobs_dodged != 0:
        #     self.try_augment_mob_velx = True
        #     if self.try_augment_mob_velx:
        #         if random.randrange(100) / 100 > .75:
        #             self.mob_velx += 1
        #         self.try_augment_mob_velx = False

            

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
        
    def draw_pentagram(self):
        for y in range(HEIGHT // 3, 2 * HEIGHT // 3, int(1 / 15 * HEIGHT)):
            
            pg.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))
    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)

        self.draw_pentagram()

        self.all_sprites.draw(self.screen)

        # *after* drawing everything, flip the display
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