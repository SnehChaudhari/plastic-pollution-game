import pygame

pygame.init()       # initializes pygame for the game

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)             # sets a specific resolution
pygame.display.set_caption("Plastic Pollution Tetris")   # sets a name at the top of the window

running = True
while running:                             # loop that quits the game if closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
