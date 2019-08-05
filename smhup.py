# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
# If you need to use this sound in your personal project, credit me as Gumichan01
# This is a pygame template sceleton for a new pygame project
import pygame
import random
import os
from os import path
from settings import *
from actors.payload import Payload
from actors.player import Player
from actors.mob import Mob
from actors.explosion import Explosion, Explosion_Animation
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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shout'em Up Space Game")
clock = pygame.time.Clock()
hit_count = 0
payload_count = 1
current_level = 1
mine_count = 3
enemy_count = ENEMY_NR_START
stage = 1
bos_time = False
shooting = False
explosion_animation = Explosion_Animation().get_explosion_images()
# Load assets
background_image = pygame.transform.scale(pygame.image.load(path.join(IMG_DIR, 'starfield.png')).convert(),(WIDTH,HEIGHT))
background_rect = background_image.get_rect()

expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(SOUND_DIR, snd)))
for snd in expl_sounds:
    snd.set_volume(EXPLOSION_VOLUME)

# Load music
pygame.mixer.music.load(path.join(SOUND_DIR,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(MUSIC_VOLUME)

# player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()

# Add our sprites
all_sprites = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
payload_group = pygame.sprite.Group()



player = Player(settings)
all_sprites.add(player)

player_mini_image = pygame.transform.scale(player.get_image(), (25,19))
player_mini_image.set_colorkey(BLACK)

payload = Payload(CENTER, Payload.EARTH_1, WIDTH, HEIGHT)
payload2 = None
all_sprites.add(payload)

payload_group.add(payload)


pygame.mixer.music.play(loops=-1)
running = True

# Process User Inputs this can be a different class as well
def process_inputs():
    global running
    global shooting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting = True
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_b:
                # DROP a mine
                pass
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shooting = False
        
def draw_lives(surf, x, y, lives, img):
    for i in range(player.lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def shoot(ready):
    if ready:
        new_bullets = player.shoot()
        if new_bullets:
            all_sprites.add(new_bullets)
            bullets_group.add(new_bullets)
    
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10 
    fil = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fil, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def check_for_payload_collissions():
    global payload_count
    global running
    payload_hit = pygame.sprite.groupcollide(payload_group, mobs_group, True, True, pygame.sprite.collide_circle)
    if payload_hit:
        for hit in payload_hit:
            add_one_mob()
            explosion = Explosion(hit.rect.center, 'lg', explosion_animation)
            all_sprites.add(explosion)
            payload_count -= 1
            if payload_count == 0:
                running = False

def check_for_bullet_collisions():
    bullet_hits = pygame.sprite.groupcollide(mobs_group, bullets_group, True, True)
    l_hit_count = 0
    for hit in bullet_hits:
        l_hit_count += 1
        explosion = Explosion(hit.rect.center, 'lg', explosion_animation)
        all_sprites.add(explosion)
        random.choice(expl_sounds).play()
    return l_hit_count

def determine_level(current_level, hit_count):
    global mine_count
    global enemy_count
    if (hit_count % LEVEL_UP) == 0:
        mine_count = 3
        current_level += 1 # Level Up
        #enemy_count += 1
        #if enemy_count < 16:
        #    add_one_mob()
        if current_level < 3 or (current_level > 4 and current_level < 6):
            player.bullet_count = Player.BULLET_COUNT_1
        else:
            player.bullet_count = Player.BULLET_COUNT_2
        if current_level == 5 and payload_count == 1:
            # Time for two moons
            add_second_earth()
        elif payload_count == 1:
            move_earth()        
        else:
            increase_earth_gap()
    return current_level

def move_earth():
    payload.target_x = random.randrange(50, WIDTH - 50, 5)

def increase_earth_gap():
    if payload != None and payload.target_x > 50:
        payload.target_x -= 20
    if payload2 != None and payload2.target_x < WIDTH - 50:
        payload2.target_x +=20     

def add_second_earth():
    global payload2
    global payload_count
    payload_count += 1
    payload.target_x = CENTER - 50
    payload2 = Payload(CENTER + 50, Payload.EARTH_2, WIDTH, HEIGHT)
    all_sprites.add(payload2)
    payload_group.add(payload2)

def add_one_mob():
    mob = Mob(settings, current_level)
    mobs_group.add(mob)
    all_sprites.add(mob)

def check_for_player_collision():
    global running
    hits = pygame.sprite.spritecollide(player, mobs_group, True, pygame.sprite.collide_circle) 
    for hit in hits:
        damage = hit.radius * 2
        explode_player = player.update_shield(damage)
        if explode_player:
            explosion = Explosion(hit.rect.center, 'lg', explosion_animation)
            player.lives -= 1
            if player.lives == 0:
                running = False
        else:
            explosion = Explosion(hit.rect.center, 'sm', explosion_animation)
            
        all_sprites.add(explosion)
        add_one_mob()

def end_of_stage_bos(stage):
    if stage == 1:
        #Create a swarm mob
        for x in range(40):
            add_one_mob()

def check_done(stage):
    if stage == 1:
        return not mobs_group
    return True #No more sprites left

def add_mob(nr):
    for i in range(nr):
        add_one_mob()

def next_stage(stage):
    # Increase Player Shield 
    if payload_count == 2:
        player.shield = 100
    else:
        player.shield = 75
    add_mob(ENEMY_NR_START + stage)

add_mob(ENEMY_NR_START)

while running:
    clock.tick(FPS)    
    # Process Input Events
    process_inputs()
    
    # Updates
    shoot(shooting)
    all_sprites.update()
    
    # check for collissions
    check_for_payload_collissions()

    # check for bullet collisions
    current_hits = check_for_bullet_collisions()
    hit_count += current_hits
    # add mob back
    if (current_hits > 0):
        if not bos_time:
            add_mob(current_hits) # replace the enemies
            current_level = determine_level(current_level, hit_count)
            if current_level > 7:
                bos_time = True
                end_of_stage_bos(stage) 
        else: 
            if check_done(stage):
                print("You did it")
                stage += 1
                current_level = 1
                bos_time = False
                next_stage(stage)
    # The boolean value is do kill if true it would remove mob from mobs_group e.g. coin pickup
    check_for_player_collision()
    
    # Render Draw
    screen.fill(BLACK)
    screen.blit(background_image, background_rect)
    all_sprites.draw(screen)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_image)
    draw_text(font_name, WHITE, screen, 'S %d L %d - Mines %d - Score %d ' % (stage, current_level, mine_count, hit_count), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    # After the drawing flip the screen to display
    pygame.display.flip()
    

print("Hits %d. Well Done!"%(hit_count))
pygame.quit()
