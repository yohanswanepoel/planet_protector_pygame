# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
# If you need to use this sound in your personal project, credit me as Gumichan01
# This is a pygame template sceleton for a new pygame project
import pygame
import random
import os
from os import path
import settings
from actors.payload import Payload
from actors.player import Player
from actors.mob import Mob
from helper.text_helpers import draw_text


# Level Up 1, 2, 3, 4 planet moves to a random location
# Level Up 1-4 things go faster
# Level 5 and up two planets move further and further appart
# Level 5 and up speed starts at 1 again and moves up
# Level 9 add a third planet??
# Add blockers that last for 10 hits - get if enough hits
# Meteors and curves every now and then?

font_name = pygame.font.match_font('arial')

# Setup the game
pygame.init()
pygame.mixer.init()
pygame.mixer.fadeout(70)
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Shout'em Up Space Game")
clock = pygame.time.Clock()
hit_count = 0
payload_count = 1
current_level = 1
mine_count = 3

# Load assets
background_image = pygame.transform.scale(pygame.image.load(path.join(settings.IMG_DIR, 'starfield.png')).convert(),(settings.WIDTH,settings.HEIGHT))
background_rect = background_image.get_rect()

expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(settings.SOUND_DIR, snd)))
for snd in expl_sounds:
    snd.set_volume(settings.EXPLOSION_VOLUME)

# Load music
pygame.mixer.music.load(path.join(settings.SOUND_DIR,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)

# player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()

# Add our sprites
all_sprites = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
payload_group = pygame.sprite.Group()

player = Player(settings)
all_sprites.add(player)

payload = Payload(settings.CENTER, Payload.EARTH_1, settings.WIDTH, settings.HEIGHT)
all_sprites.add(payload)

payload_group.add(payload)

for i in range(settings.ENEMY_NR_START):
    mob = Mob(settings, current_level)
    mobs_group.add(mob)
    all_sprites.add(mob)

pygame.mixer.music.play(loops=-1)
running = True

while running:
    clock.tick(settings.FPS)    
    # Process Input Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_bullets = player.shoot()
                all_sprites.add(new_bullets)
                bullets_group.add(new_bullets)
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_b:
                # DROP a mine
                pass

    # Updates
    all_sprites.update()

    # check for collissions
    payload_hit = pygame.sprite.groupcollide(payload_group, mobs_group, True, True, pygame.sprite.collide_circle)
    if payload_hit:
        payload_count -= 1
        if payload_count == 0:
            running = False

    # check for bullet collisions
    bullet_hits = pygame.sprite.groupcollide(mobs_group, bullets_group, True, True)
    for hit in bullet_hits:
        hit_count += 1
        random.choice(expl_sounds).play()
        if hit_count % settings.LEVEL_UP == 0:
            print("Level Up")
            mine_count = 3
            current_level += 1 # Level Up
            if current_level < 3 or (current_level > 4 and current_level < 6):
                player.bullet_count = Player.BULLET_COUNT_1
            else:
                player.bullet_count = Player.BULLET_COUNT_2
            if current_level == 5:
                # Time for two moons
                payload.target_x = settings.CENTER - 50
                payload2 = Payload(settings.CENTER + 50, Payload.EARTH_2, settings.WIDTH, settings.HEIGHT)
                all_sprites.add(payload2)
                payload_group.add(payload2)
            elif current_level < 5:
                payload.target_x = random.randrange(50, settings.WIDTH - 50, 5)
            else:
                if payload.target_x > 50:
                    payload.target_x -= 5
                if payload2.target_x < settings.WIDTH - 50:
                    payload2.target_x +=5 
        if hit_count < settings.REQUIRED_HITS:
            mob = Mob(settings, current_level)
            mobs_group.add(mob)
            all_sprites.add(mob)
        elif hit_count >= settings.REQUIRED_HITS:
            running = False
        

    # The boolean value is do kill if true it would remove mob from mobs_group e.g. coin pickup
    hits = pygame.sprite.spritecollide(player, mobs_group, False, pygame.sprite.collide_circle) 
    if hits:
        running = False

    # hit_count is now high create another payload
    

    # Render Draw
    screen.fill(settings.BLACK)
    screen.blit(background_image, background_rect)
    all_sprites.draw(screen)
    draw_text(font_name, settings.WHITE, screen, 'Level %d - Mines %d - Hits %d ' % (current_level, mine_count, hit_count), 18, settings.WIDTH / 2, 10)
    # After the drawing flip the screen to display
    pygame.display.flip()
    

print("Hits %d. Well Done!"%(hit_count))
pygame.quit()
