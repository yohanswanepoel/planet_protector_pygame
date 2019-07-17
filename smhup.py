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
enemy_count = settings.ENEMY_NR_START

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
payload2 = None
all_sprites.add(payload)

payload_group.add(payload)

for i in range(settings.ENEMY_NR_START):
    mob = Mob(settings, current_level)
    mobs_group.add(mob)
    all_sprites.add(mob)

pygame.mixer.music.play(loops=-1)
running = True

# Process User Inputs this can be a different class as well
def process_inputs():
    global running
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

def check_for_payload_collissions():
    global payload_count
    global running
    payload_hit = pygame.sprite.groupcollide(payload_group, mobs_group, True, True, pygame.sprite.collide_circle)
    if payload_hit:
        add_one_mob()
        payload_count -= 1
        if payload_count == 0:
            running = False

def check_for_bullet_collisions():
    bullet_hits = pygame.sprite.groupcollide(mobs_group, bullets_group, True, True)
    l_hit_count = 0
    for hit in bullet_hits:
        l_hit_count += 1
        random.choice(expl_sounds).play()
    return l_hit_count

def determine_level(current_level, hit_count):
    global mine_count
    global enemy_count
    if (hit_count % settings.LEVEL_UP) == 0:
        mine_count = 3
        current_level += 1 # Level Up
        enemy_count += 1
        if enemy_count < 16:
            add_one_mob()
        if current_level < 3 or (current_level > 4 and current_level < 6):
            player.bullet_count = Player.BULLET_COUNT_1
        else:
            player.bullet_count = Player.BULLET_COUNT_2
        if current_level == 5:
            # Time for two moons
            add_second_earth()
        elif payload_count == 1:
            move_earth()        
        else:
            increase_earth_gap()
    return current_level

def move_earth():
    payload.target_x = random.randrange(50, settings.WIDTH - 50, 5)

def increase_earth_gap():
    if payload != None and payload.target_x > 50:
        payload.target_x -= 5
    if payload2 != None and payload2.target_x < settings.WIDTH - 50:
        payload2.target_x +=5     

def add_second_earth():
    global payload2
    global payload_count
    payload_count += 1
    payload.target_x = settings.CENTER - 50
    payload2 = Payload(settings.CENTER + 50, Payload.EARTH_2, settings.WIDTH, settings.HEIGHT)
    all_sprites.add(payload2)
    payload_group.add(payload2)

def add_one_mob():
    mob = Mob(settings, current_level)
    mobs_group.add(mob)
    all_sprites.add(mob)

def add_mob_back(current_hits, current_level):
    for x in range(current_hits):
        mob = Mob(settings, current_level)
        mobs_group.add(mob)
        all_sprites.add(mob)

def check_for_player_collision():
    global running
    hits = pygame.sprite.spritecollide(player, mobs_group, True, pygame.sprite.collide_circle) 
    for hit in hits:
        damage = hit.radius * 2
        running = player.update_shield(damage)
        add_one_mob()

while running:
    clock.tick(settings.FPS)    
    # Process Input Events
    process_inputs()

    # Updates
    all_sprites.update()

    # check for collissions
    check_for_payload_collissions()

    # check for bullet collisions
    current_hits = check_for_bullet_collisions()
    # add mob back
    if (current_hits > 0):
        add_mob_back(current_hits, current_level)
        # determine level
        hit_count += current_hits
        current_level = determine_level(current_level, hit_count)    

    # The boolean value is do kill if true it would remove mob from mobs_group e.g. coin pickup
    check_for_player_collision()
    
    # Render Draw
    screen.fill(settings.BLACK)
    screen.blit(background_image, background_rect)
    all_sprites.draw(screen)
    draw_text(font_name, settings.WHITE, screen, 'Level %d - Mines %d - Hits %d - Shield %d' % (current_level, mine_count, hit_count, player.shield), 18, settings.WIDTH / 2, 10)
    # After the drawing flip the screen to display
    pygame.display.flip()
    

print("Hits %d. Well Done!"%(hit_count))
pygame.quit()
