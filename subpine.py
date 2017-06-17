import pygame, sys, os, time, datetime, urllib
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

# Set up the screen

DISPLAYSURF = pygame.display.set_mode((320, 240), 0, 16)
pygame.mouse.set_visible(0)
pygame.display.set_caption('Stats')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN  = (  0, 255, 255)

# Main loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    currentime = datetime.datetime.time(datetime.datetime.now())

    # Draw the title

    black_square_that_is_the_size_of_the_screen = pygame.Surface(DISPLAYSURF.get_size())
    black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
    DISPLAYSURF.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

    font = pygame.font.Font(None, 40)
    text = font.render("Outside", 1, RED)
    textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/4+13)
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 40)
    text = font.render("Inside", 1, RED)
    textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/4+179)
    DISPLAYSURF.blit(text, textpos)

    # Draw Lines

    pygame.draw.line(DISPLAYSURF, GREEN, [5, 140], [DISPLAYSURF.get_width()-5, 140], 1)

    pygame.draw.line(DISPLAYSURF, GREEN, [DISPLAYSURF.get_width()/2+30, 5], [DISPLAYSURF.get_width()/2+30, 140], 1)

    clock.tick()
    font = pygame.font.Font(None, 75)
    text = font.render("{0:.2f} fps".format(clock.get_fps()), 1, CYAN)
    textpos = text.get_rect(center=(DISPLAYSURF.get_width() / 2, 215))
    DISPLAYSURF.blit(text, textpos)

    pygame.display.update()

