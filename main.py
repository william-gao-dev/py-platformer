# William Gao
# Jumpy! - platform game

import pygame as pg ## pygame == pg
import random
import time

from gameSettings import *
from sprites import *
from os import path

# self.playing defines whether game loop will running
# self.running defines whether entire program will run

class Game:
    def __init__(self):
        # Initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode ((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_assets()
        self.last_update =  0
        self.quit_attempts = 0
        self.channel1 = pg.mixer.Channel(1) # jump and collision sound effects
        self.channel2 = pg.mixer.Channel(2) # startscreen and ambient music
        self.channel3 = pg.mixer.Channel(3) # powerup sound effects
        self.channel4 = pg.mixer.Channel(4)

    def load_assets(self):
        # high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,'img')
        with open(path.join(self.dir, HIGHSCORE_FILE), 'r+') as f:
            try: # Try reading file,
                self.highscore = int(f.read())
            except: # If theres nothing in the file, set highscore to 0.
                self.highscore = 0
        # load spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))


        # load sounds

        self.snd_dir = path.join(self.dir,'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir,JUMP_SOUND))
        self.start_screen_sound = pg.mixer.Sound(path.join(self.snd_dir,START_SCREEN_MUSIC))
        self.boost_powerup_sound1 = pg.mixer.Sound(path.join(self.snd_dir,BOOST_POWERUP_SOUND1))
        self.boost_powerup_sound2 = pg.mixer.Sound(path.join(self.snd_dir,BOOST_POWERUP_SOUND2))


    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.platforms2 = pg.sprite.Group()
        self.platforms3 = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.player = Player(self)
        for platforms in PLATFORM_LIST:
            Platform(self,*platforms) # Exploding a PLATFORM_LIST
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.load(path.join(self.snd_dir,AMBIENT_SOUND))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(AMBIENT_SOUND_VOLUME)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if lowest.rect.bottom < hit.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right and \
                    self.player.pos.x > lowest.rect.left:
                    if self.player.pos.y < hits[0].rect.top+30:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        # If player reaches top quarter of the screen
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += abs(self.player.vel.y)
            for platform in self.platforms:
                platform.rect.y += abs(self.player.vel.y)
                if platform.rect.top >= HEIGHT+5:
                    platform.kill()
                    self.score +=10
        # If player dies
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        # spawn new platforms to keep same average number of platforms
        LASTWIDTH = 0
        while len(self.platforms) < 7:
            width = random.randrange(0,100)
            if width in range(LASTWIDTH-20,LASTWIDTH+20):
                width = width + 20
                PLATFORMWIDTH = WIDTH-width
                p = Platform(self,random.randrange(0,PLATFORMWIDTH),
                        random.randrange(-75,-30))
            else:
                PLATFORMWIDTH = WIDTH-width
                p = Platform(self,random.randrange(0,PLATFORMWIDTH),
                        random.randrange(-75,-30))
            LASTWIDTH = width
        # Check for player sprite collision with a powerup sprite
        powerupHits = pg.sprite.spritecollide(self.player,self.powerups, True)
        powerupDuration = 0
        for pow in powerupHits:
            if pow.type == 'boost':
                self.channel3.set_volume(BOOST_POWERUP_VOLUME1)
                self.channel3.play(self.boost_powerup_sound1)
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
                powerupDuration = 1

            if powerupDuration == 1:
                self.channel3.set_volume(BOOST_POWERUP_VOLUME2)
                self.channel3.play(self.boost_powerup_sound2)


    def events(self):
        # Game Loop - Events
        # For infinite jumping
        # now = pg.time.get_ticks()
        # if now - self.last_update > 350:
        #     self.last_update = now
        #     self.player.jump()
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_ESCAPE:
                    self.quit_attempts += 1
                    if self.quit_attempts == 2:
                        pg.quit()
                        quit()


            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()


    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image,self.player.rect)
        self.draw_text(str(self.score),22,WHITE,20,13)
        pg.display.flip()

    def show_start_screen(self):
        # Game splash/start screen
        self.channel2.set_volume(START_SCREEN_VOLUME)
        self.channel2.play(self.start_screen_sound)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Arrow keys move, Space to jump",22,WHITE,WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play",22,WHITE,WIDTH/2,HEIGHT*3/4)
        self.draw_text("High Score: " +str(self.highscore),22,WHITE,WIDTH/2,15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # Gameover / continue
        if self.running == False:
            return
        self.channel2.set_volume(START_SCREEN_VOLUME)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER",48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Score: " + str(self.score) ,22,WHITE,WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again",22,WHITE,WIDTH/2,HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH/2, HEIGHT /2 + 40)
            with open(path.join(self.dir,HIGHSCORE_FILE),'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " +str(self.highscore),22,WHITE,WIDTH/2,HEIGHT/2+40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    time.sleep(0.2)
                    waiting = False
                    self.channel2.set_volume(0)
                    self.running = True

    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
quit()
