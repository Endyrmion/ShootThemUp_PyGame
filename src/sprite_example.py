#Pygame template - skeleton for a new pygame project
import pygame
import os
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

# Some usefull colors for my program
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# setting up the assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


class Player(pygame.sprite.Sprite):
    # sprite of the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "p1_jump.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


# this chunk of code initialize the window and the window data
pygame.init() #init pygame
pygame.mixer.init() #mixer enable the sound in the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Awesome Game")
clock = pygame.time.Clock()

# Create a Sprite Group to make the display of the sprites easyer
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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


    # The Drawing or The Render
    screen.fill(WHITE)
    all_sprites.draw(screen)


    # after drawing everything, flip the display (DBM)
    pygame.display.flip() # double buffering method

pygame.quit()
