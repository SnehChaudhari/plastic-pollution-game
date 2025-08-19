import pygame
import sys
import random

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

# scoring and level variables
score = 0
level = 1
lines_cleared_total = 0

# game over boolean
game_over = False

# font for score/level
font = pygame.font.SysFont(None, 36)

# setup display using default resolution
screen = pygame.display.set_mode((screen_width, screen_height))

# sets a name at the top of the window
pygame.display.set_caption("Plastic Pollution Tetris")

# load and scale the background image
background = pygame.image.load("ocean_background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# tetromino dictionary (7 shapes)
tetromino_shapes = [
    {"blocks": [(0, 1), (1, 1), (2, 1), (3, 1)], "colour": "cyan"},     # I
    {"blocks": [(1, 0), (0, 1), (1, 1), (2, 1)], "colour": "blue"},     # T
    {"blocks": [(0, 0), (0, 1), (1, 1), (2, 1)], "colour": "orange"},   # L
    {"blocks": [(2, 0), (0, 1), (1, 1), (2, 1)], "colour": "red"},      # J
    {"blocks": [(1, 0), (2, 0), (0, 1), (1, 1)], "colour": "green"},    # S
    {"blocks": [(0, 0), (1, 0), (1, 1), (2, 1)], "colour": "yellow"},   # Z
    {"blocks": [(0, 0), (1, 0), (0, 1), (1, 1)], "colour": "purple"}    # O
            ]

# ticks for gravity (miliseconds)
fall_speed = 500
last_fall_time = pygame.time.get_ticks()

# tick delay for movement
move_delay = 150
last_move_time = pygame.time.get_ticks()

# list to store frozen blocks
frozen_blocks = []    # (x, y, colour)

# game state, used for determining if the game is
# paused, in main menu, ended, or playing.
game_state = "menu"     # "menu", "end", "playing", "paused"

# function for making new tetromino from any of the shapes
def new_tetromino():
    shape = random.choice(tetromino_shapes)
    return {
        "blocks": [(x + grid_width // 2 - 2, y) for x, y in shape["blocks"]],
        "colour": shape["colour"]
            }

# function to draw game over screen
def draw_game_over():

    # main text
    game_over_text = font.render("GAME OVER", True, "white")
    restart_text = font.render("Press R to Restart", True, "white")
    menu_text = font.render("Press M to go back to Menu", True, "white")

    # stats text
    score_text = font.render(f"Final Score: {score}", True, "white")
    level_text = font.render(f"Level Reached: {level}", True, "white")
    lines_text = font.render(f"Lines Cleared: {lines_cleared_total}", True, "white")

    # draw texts
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2,
                                 screen_height // 2 - 120))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2,
                                 screen_height // 2 - 60))
    screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2,
                                 screen_height // 2 - 30))
    screen.blit(lines_text, (screen_width // 2 - lines_text.get_width() // 2,
                                 screen_height // 2))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2,
                               screen_height // 2 + 60))
    screen.blit(menu_text, (screen_width // 2 - menu_text.get_width() // 2,
                               screen_height // 2 + 90))

# function to draw pause screen
def draw_pause():
    pause_text = font.render("PAUSED", True, "white")
    resume_text = font.render("Press P to Resume", True, "white")
    screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height / 2 - 50))
    screen.blit(resume_text, (screen_width // 2 - resume_text.get_width() // 2, screen_height // 2))

# rotation control 
def rotate_tetromino(tetromino):
    # just a placeholder for now
    blocks = tetromino["blocks"]
    # use the second block as the center of rotation
    center_x, center_y = blocks[1]

    rotated_blocks = []
    for x, y in blocks:
        # translate point to origin, rotate, then translate back
        rel_x, rel_y = x - center_x, y - center_y
        new_x = center_x - rel_y
        new_y = center_y + rel_x
        rotated_blocks.append((new_x, new_y))

        # collision detection
    if not check_collision(rotated_blocks):
        tetromino["blocks"] = rotated_blocks

# function for restarting the game
def restart_game():
    global score, level, lines_cleared_total, frozen_blocks, tetromino, game_over, fall_speed, last_fall_time
    score = 0
    level = 1
    lines_cleared_total = 0
    frozen_blocks = []
    tetromino = new_tetromino()
    game_over = False
    fall_speed = 500
    last_fall_time = pygame.time.get_ticks()

# for current falling tetromino
tetromino = new_tetromino()

# function for drawing grid
def draw_grid():
    for row in range(grid_height):
        for col in range(grid_width):
            rect = pygame.Rect(grid_x + col * cell_size, grid_y + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, "grey", rect, 1)   # 1 pixel border

# function for drawing tetromino
def draw_tetromino(tetromino_shapes):
    for x, y in tetromino_shapes["blocks"]:
        rect = pygame.Rect(grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, tetromino_shapes["colour"], rect)

# function for drawing frozen blocks
def draw_frozen_blocks():
    for x, y, colour in frozen_blocks:
        rect = pygame.Rect(grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, colour, rect)

# function for checking collision of blocks
def check_collision(blocks):
    for x, y in blocks:
        if x < 0 or x >= grid_width or y >= grid_height:
            return True
        if (x, y) in [(bx, by) for bx, by, _ in frozen_blocks]:
            return True
    return False

# function for moving tetromino down (gravity)
def move_tetromino_down(tetromino_shapes):
    moved_blocks = [(x, y + 1) for x, y in tetromino["blocks"]]
    if not check_collision(moved_blocks):
        tetromino["blocks"] = moved_blocks
        return True
    return False

# function for stacking the falling tetromino onto already frozen blocks
def stack_tetromino(tetromino):
    for x, y in tetromino["blocks"]:
        frozen_blocks.append((x, y, tetromino["colour"]))
    clear_lines()

# function to clear full lines (horizontally)
def clear_lines():
    global frozen_blocks, score, level, lines_cleared_total, fall_speed
    new_frozen = []
    rows = [y for _, y, _ in frozen_blocks]
    full_rows = []

    for y in range(grid_height):
        if rows.count(y) >= grid_width:
            full_rows.append(y)

    if full_rows:
        for x, y, colour in frozen_blocks:
            if y not in full_rows:
                # count how many cleared rows are below the current y
                shift = sum(1 for row in full_rows if row > y)
                new_frozen.append((x, y + shift, colour))
        frozen_blocks = new_frozen

    # score counting section
    lines_cleared = len(full_rows)
    score += lines_cleared * 100
    lines_cleared_total += lines_cleared
    # level progression
    if lines_cleared_total >= level * 5: # every 5 lines
        level += 1
        fall_speed = max(100, fall_speed - 50) # blocks fall faster

def draw_score_level():
    score_text = font.render(f"Score: {score}", True, "white")
    level_text= font.render(f"Level: {level}", True, "white")
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 60))

# function for moving tetromino sideways (with grid collision checker)
def move_tetromino_sideways(tetromino, dx):
    new_blocks = [(x + dx, y) for x, y in tetromino["blocks"]]
    # collision detection
    if not check_collision(new_blocks):
        tetromino["blocks"] = new_blocks

# function to handle movement input
# has a cooldown now
def handle_input(tetromino):
    global last_move_time
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time > move_delay:
        if keys[pygame.K_LEFT]:
            move_tetromino_sideways(tetromino, -1)
            last_move_time = current_time
        elif keys[pygame.K_RIGHT]:
            move_tetromino_sideways(tetromino, 1)
            last_move_time = current_time
        elif keys[pygame.K_DOWN]:
            move_tetromino_down(tetromino)
            last_move_time = current_time

# function for drawing menu
def draw_menu():
    title = font.render("Plastic Pollution Tetris", True, "white")
    prompt = font.render("Press ENTER to Start", True, "white")
    screen.blit(title, (screen_width//2 - title.get_width()//2, screen_height//2 - 60))
    screen.blit(prompt, (screen_width//2 - prompt.get_width()//2, screen_height//2))
            
# main game loop
running = True
while running:

    # draws background image
    screen.blit(background, (0, 0))
    
    # loop that quits the game cleanly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # implementing menu function
        if game_state == "menu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                restart_game()
                game_state = "playing"
        
        # rotate key calling function
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotate_tetromino(tetromino)
                elif event.key == pygame.K_p:
                    game_state = "paused"

        # pause game calling function            
        elif game_state == "paused":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                game_state = "playing"

        # implementing restart function
        elif game_state == "end":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
                game_state = "playing"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                game_state = "menu"

    # drawing menu
    if game_state == "menu":
        draw_menu()

    # wrapping everything in game_state playing loop
    elif game_state == "playing":
        
        # calling controls function
        handle_input(tetromino)
    
        # gravity timing using ticks (miliseconds)
        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > fall_speed:
            #collision detection
            if not move_tetromino_down(tetromino):
                stack_tetromino(tetromino)
                tetromino = new_tetromino()
                if check_collision(tetromino["blocks"]):
                    game_state = "end"
            last_fall_time = current_time

        # use functions to draw grid and tetrominos
        draw_grid()
        draw_tetromino(tetromino)

        # use function to draw frozen blocks
        draw_frozen_blocks()

        # use function to draw score
        draw_score_level()

    # calling the function to draw pause screen
    elif game_state == "paused":
        draw_pause()
            
    # calling the draw game over function
    elif game_state == "end":
        draw_game_over()

    # updates the background (for the image)
    pygame.display.flip()
    
pygame.quit()
