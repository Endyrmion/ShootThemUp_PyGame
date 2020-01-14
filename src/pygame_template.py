#Pygame template - skeleton for a new pygame project
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

# Some usefull colors for my program
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# this chunk of code initialize the window and the window data
pygame.init() #init pygame
pygame.mixer.init() #mixer enable the sound in the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Awesome Game")
clock = pygame.time.Clock()

# Create a Sprite Group to make the display of the sprites easyer
all_sprites= pygame.sprite.Group()

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
    screen.fill(BLACK)
    all_sprites.draw(screen)


    # after drawing everything, flip the display (DBM)
    pygame.display.flip() # double buffering method

pygame.quit()
