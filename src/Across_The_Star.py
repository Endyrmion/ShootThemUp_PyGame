#Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 700
FPS = 60

# Some usefull colors for my program
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DRAK_BLUE = (0, 0, 139)


# this chunk of code initialize the window and the window data
pygame.init() #init pygame
pygame.mixer.init() #mixer enable the sound in the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Across The Star")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def spawnMeteor():
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

def draw_shield_bar(surface, x, y, value):
    if value < 0:
        value = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (value / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, DRAK_BLUE, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 30
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 0
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -9
        if keystate[pygame.K_RIGHT]:
            self.speedx = 9
        if keystate[pygame.K_UP]:
            self.speedy = -9
        if keystate[pygame.K_DOWN]:
            self.speedy = 9
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Constraints to stay in the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mob_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, - 40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, - 40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# load all graphics
background = pygame.image.load(path.join(img_dir, "space_background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "player-1.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laser.png")).convert()
mob_images = []
mob_list = ["mob.png", "mob1.png", "mob2.png", "mob3.png", "mob4.png"]
for img in mob_list:
    mob_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    # {} is a dictionnary, and instead of a list each member has a name instead of a number
explosion_animation = {}
explosion_animation['lrg'] = []
explosion_animation['sml'] = []
for i in range(9):
    filename = 'expl{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lrg = pygame.transform.scale(img, (75, 75))
    explosion_animation['lrg'].append(img_lrg)
    img_sml = pygame.transform.scale(img, (32, 32))
    explosion_animation['sml'].append(img_sml)

# sound manager
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
expl_sounds = []
for snd in ['Explosion.wav', 'Explosion2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'Space Atmosphere.mp3'))
pygame.mixer.music.set_volume(0.4)



# Create a Sprite Group to make the display of the sprites easier
# Creating different groups allow to pygame to show if one member of a group is collided by another one :)
all_sprites= pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)



for i in range(20):
    spawnMeteor()

score = 0
pygame.mixer.music.play(loops=-1)

# About the Game Loop
running = True
while running:
    # Keep the "Running" at the right speed, The Right FPS
    clock.tick(FPS)

    # The Input (or Events)
    for event in pygame.event.get():
        # Check for Closing the window.
        if event.type == pygame.QUIT:
            running = False

    # The Update
    all_sprites.update()

    # Collision management

    # if a Bullet has hit a mob :)
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lrg')
        all_sprites.add(expl)
        spawnMeteor()

    # sprite collide is a function that return a list that any hit has been occured
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sml')
        all_sprites.add(expl)
        spawnMeteor()
        if player.shield <= 0:
            running = False


    # The Drawing or The Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)


    # after drawing everything, flip the display (DBM)
    pygame.display.flip() # double buffering method

pygame.quit()
