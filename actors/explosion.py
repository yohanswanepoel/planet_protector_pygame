import pygame
import random
from os import path

class Explosion_Animation:
    BLACK = (0, 0, 0)
    EXPLOSION_ANIM = {}
    EXPLOSION_ANIM['lg'] = []
    EXPLOSION_ANIM['sm'] = []

    def __init__(self):
        for i in range(9):
            filename = 'explosion/regularExplosion0%d.png' % (i)
            img = pygame.image.load(path.join(path.dirname(__file__), filename)).convert()
            img.set_colorkey(self.BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            img_sm = pygame.transform.scale(img, (32, 32))
            self.EXPLOSION_ANIM['lg'].append(img_lg)
            self.EXPLOSION_ANIM['sm'].append(img_sm)
    
    def get_explosion_images(self):
        return self.EXPLOSION_ANIM

class Explosion(pygame.sprite.Sprite):

    FRAME_RATE = 50
    ARRAY_LEN = 0

    def __init__(self, center, size, explosion_animation):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion_animation = explosion_animation
        self.image = self.explosion_animation[self.size][0]
        self.frame = 0
        self.ARRAY_LEN = len(self.explosion_animation[self.size])
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_upate = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_upate > self.frame_rate:
            self.last_upate = now
            self.frame += 1
            if self.frame == self.ARRAY_LEN:
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
