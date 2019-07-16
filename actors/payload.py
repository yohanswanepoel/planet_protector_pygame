import pygame
import random
from os import path




class Payload(pygame.sprite.Sprite):

    EARTH_1 = 1
    EARTH_2 = 2
    PLAYER_SPEED = 5
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0

    def __init__(self, x, earth, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width
        if earth == self.EARTH_1:
            earth1_image = pygame.image.load(path.join(path.dirname(__file__), 'payload/earth1.png')).convert()
            self.image = pygame.transform.scale(earth1_image, (40,35))
        elif earth == self.EARTH_2:
            earth2_image = pygame.image.load(path.join(path.dirname(__file__), 'payload/earth2.png')).convert()
            self.image = pygame.transform.scale(earth2_image, (35,30))
        else:
            self.image = pygame.Surface((50, 30))
        self.rect = self.image.get_rect()
        self.radius = 16
        self.rect.centerx = x
        self.rect.bottom = self.SCREEN_HEIGHT - 5
        self.target_x = x
        self.speedx = 0
    
    def update(self):
        if self.rect.centerx < self.target_x:
            self.speedx = self.PLAYER_SPEED
        elif self.rect.centerx > self.target_x:
            self.speedx = -self.PLAYER_SPEED
        else:
            self.speedx = 0 
        self.rect.x += self.speedx