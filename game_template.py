# This is a pygame template sceleton for a new pygame project
import pygame
import random
import os



WIDTH = 360 #width of the game window
HEIGHT = 480 #height of the game window
FPS = 30 #frames per second that the game runs

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.image.set_colorkey(BLACK) # Create transparency for us
    
    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Johan Game")

# SET The assets folder
game_folder = os.path.dirname(__file__) # gives us the folder that this file is running from
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()

clock = pygame.time.Clock()
# Add our sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)    
    # Process Input Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Updates
    all_sprites.update()

    # Render Draw
    screen.fill(BLUE)
    all_sprites.draw(screen)
    # After the drawing flip the screen to display
    pygame.display.flip()
    
pygame.quit()



