import pygame
import random
from os import path

class Mob(pygame.sprite.Sprite):
    BLACK = (0, 0, 0)
    ENEMY_SPEEDY_MAX_L1 = 5
    ENEMY_SPEEDY_MAX_L2 = 7
    ENEMY_SPEEDY_MAX_L3 = 9
    ENEMY_SPEEDY_MAX_TO_FAST = 11
    ENEMY_SPEEDY_MIN = 1
    ENEMY_SPEEDY_MIN_2 = 3
    METEOR_MIN = 20
    METEOR_MAX = 55
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0
    METEOR_IMAGE = None

    def __init__(self, settings, current_level):
        pygame.sprite.Sprite.__init__(self)
        met_size = random.randrange(self.METEOR_MIN, self.METEOR_MAX)
        self.SCREEN_HEIGHT = settings.HEIGHT
        self.SCREEN_WIDTH = settings.WIDTH
        self.METEOR_IMAGE = pygame.image.load(path.join(path.dirname(__file__), 'mob/meteorBrown_med1.png')).convert()
        self.orig_image = pygame.transform.scale(self.METEOR_IMAGE, (met_size, met_size))
        self.orig_image.set_colorkey(self.BLACK)
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(met_size * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -40) # Spawn Off Screen
        # Increase max speed for different levels... Restart when level goes to two earths
        if current_level == 1 or current_level == 5:
            self.speedy = random.randrange(self.ENEMY_SPEEDY_MIN, self.ENEMY_SPEEDY_MAX_L1)
        elif current_level == 2 or current_level == 6:
            self.speedy = random.randrange(self.ENEMY_SPEEDY_MIN, self.ENEMY_SPEEDY_MAX_L2)
        elif current_level == 3 or current_level == 7:
            self.speedy = random.randrange(self.ENEMY_SPEEDY_MIN_2, self.ENEMY_SPEEDY_MAX_L3)
        elif current_level == 4 or current_level > 7:
            self.speedy = random.randrange(self.ENEMY_SPEEDY_MIN_2, self.ENEMY_SPEEDY_MAX_TO_FAST)
        self.speedx = random.randrange(-3, 3)
        # Lets make the Mob rotate
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.top > self.SCREEN_HEIGHT + 10) or \
            (self.rect.left > self.SCREEN_WIDTH + 10) or \
            (self.rect.right < -10):
            self.rect.x = random.randrange(self.SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40) # Spawn Off Screen
            self.speedy = random.randrange(1, 8)
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 # make sure rotation is always less than 360
            new_image = pygame.transform.rotate(self.orig_image, self.rot)
            # lots of code to make rotations smooth by recentering the rect
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
