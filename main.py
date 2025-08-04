import pygame
import sys

# initialises pygame for the game
pygame.init()

# screen resolutions
screen_width = 1280     
screen_height = 720

# grid sizes (can be expiremented with and changed later)
grid_width = 10
grid_height = 20

# grid blocks sizes (can be expiremented with and changed later)
cell_size = 32
grid_pixel_width = grid_width * cell_size
grid_pixel_height = grid_height * cell_size

# grid starting position (where it starts to get drawn)
# with basic maths (finding midpoint) we can find the centre of the screen
grid_x = (screen_width - grid_pixel_width) / 2
grid_y = (screen_height - grid_pixel_height) / 2

# our very first tetromino (placed in the center as an example
tetromino1 = [(4, 0), (4, 1), (4, 2), (4, 3)]

# makes the window resizable (with the default screen resolution)
screen = pygame.display.set_mode((screen_width, screen_height))

# sets a name at the top of the window
pygame.display.set_caption("Plastic Pollution Tetris")

# load and scale the background image
background = pygame.image.load("ocean_background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# function for drawing grid
def draw_grid():
    for row in range(grid_height):
        for col in range(grid_width):
            rect = pygame.Rect(grid_x + col * cell_size, grid_y + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, "grey", rect, 1)   # 1 pixel border

# function for drawing tetromino
def draw_tetromino(blocks, colour):
    for x, y in blocks:
        rect = pygame.Rect(grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, colour, rect)

# main game loop
running = True
while running:

    # loop that quits the game cleanly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # draws background image
    screen.blit(background, (0, 0))

    # use functions to draw grid and our tetromino
    draw_grid()
    draw_tetromino(tetromino1, "cyan")

    # updates the background (for the image)
    pygame.display.flip()

pygame.quit()
