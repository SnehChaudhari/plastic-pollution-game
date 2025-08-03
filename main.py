import pygame

# initialises pygame for the game
pygame.init()

# screen resolutions
screen_width = 1280     
screen_height = 720

# makes the window resizable (with the default screen resolution)
screen = pygame.display.set_mode((screen_width, screen_height))

# sets a name at the top of the window
pygame.display.set_caption("Plastic Pollution Tetris")

# load and scale the background image
background = pygame.image.load("ocean_background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# main game loop
running = True
while running:

    # loop that quits the game cleanly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # draws background image
    screen.blit(background, (0, 0)) 

    # updates the background (for the image)
    pygame.display.flip()

pygame.quit()
