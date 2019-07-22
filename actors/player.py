import pygame
import random
from os import path
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    PLAYER_SPEED = 5
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0
    BULLET_COUNT_1 = 1
    BULLET_COUNT_2 = 2
    BLACK = (0, 0, 0)
    SHOOT_SOUND_1 = None
    SHOOT_SOUND_2 = None
    SHIELD = 100
    SHOOT_DELAY = 200

    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_count = 1
        self.PLAYER_SPEED = settings.PLAYER_SPEED
        self.SCREEN_WIDTH = settings.WIDTH
        self.SCREEN_HEIGHT = settings.HEIGHT
        self.shield = self.SHIELD
        self.shoot_delay = self.SHOOT_DELAY
        self.last_shot = pygame.time.get_ticks()
        self.SHOOT_SOUND_1 = pygame.mixer.Sound(path.join(path.dirname(__file__), 'player/laser.wav'))
        self.SHOOT_SOUND_1.set_volume(settings.GUN_VOLUME)
        self.SHOOT_SOUND_2 = pygame.mixer.Sound(path.join(path.dirname(__file__), 'player/laser2.wav'))
        self.SHOOT_SOUND_2.set_volume(settings.GUN_VOLUME)
        self.player_image = pygame.image.load(path.join(path.dirname(__file__), 'player/playerShip1_orange.png')).convert()
        self.image = pygame.transform.scale(self.player_image, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.image.set_colorkey(self.BLACK)
        self.rect.centerx = self.SCREEN_WIDTH / 2
        self.rect.bottom = self.SCREEN_HEIGHT - 50
        self.speedx = 0
        # self.image.set_colorkey(BLACK) # Create transparency for us
    
    def update(self):
        # Sprite will always stand still unless we press a key
        self.speedx = 0
        key_state = pygame.key.get_pressed() #returns an array
        if key_state[pygame.K_LEFT]:
            if self.rect.left < 0:
                self.left = 0
            else:
                self.speedx = -self.PLAYER_SPEED
        if key_state[pygame.K_RIGHT]:
            if self.rect.right > self.SCREEN_WIDTH:
                self.righ = self.SCREEN_WIDTH
            else:
                self.speedx = self.PLAYER_SPEED
        self.rect.x += self.speedx
    
    def update_shield(self, damage):
        self.shield -= damage
        if (self.shield <= 0):
            return False #Player is dead
        return True #Player is still alive

    def shoot(self):
        # Level 1 and 2 shoot  1 bullet
        # @TODO when two earth start do we keep two bullets?
        #if current_level < 3 or (current_level > 4 and current_level < 6):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.bullet_count == self.BULLET_COUNT_1:
                bullet = Bullet(self.rect.centerx, self.rect.top + 5)
                self.SHOOT_SOUND_1.play()
                return bullet
            else:
                bullet_l = Bullet(self.rect.left, self.rect.top + 8)
                bullet_r = Bullet(self.rect.right, self.rect.top + 8)
                self.SHOOT_SOUND_2.play()
                return bullet_l, bullet_r

