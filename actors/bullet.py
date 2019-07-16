import pygame
import random
from os import path

class Bullet(pygame.sprite.Sprite):
    PLAYER_SPEED = 5
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0
    BULLET_COUNT_1 = 1
    BULLET_COUNT_2 = 2
    BULLET_SPEED = 10
    BLACK = (0, 0, 0)
    bullet_image = None

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_image= bullet_image = pygame.image.load(path.join(path.dirname(__file__), 'player/laserRed16.png')).convert()
        self.image = pygame.transform.scale(self.bullet_image, (10,20))
        self.image.set_colorkey(self.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -self.BULLET_SPEED
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()