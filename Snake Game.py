import pygame
import random
import math
from snake import Snake  # assuming snake.py is in the same directory

# Constants
WIDTH = 640
HEIGHT = 640
PIXELS = 32
SQUARES = int(WIDTH / PIXELS)
BG1 = (156, 210, 54)
BG2 = (147, 203, 57)

# Snake 
snake = Snake("Player 1")

# Food
food_pos_x = random.randrange(0, WIDTH - PIXELS, 32)
food_pos_y = random.randrange(0, HEIGHT - PIXELS, 32)

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
score_value = 0
scoreboard_x_coord = 240
scoreboard_y_coord = 5

# Functions
def draw_background(screen):
    screen.fill(BG1)
    counter = 0
    for row in range(SQUARES):
        for col in range(SQUARES):
            if counter % 2 == 0:
                pygame.draw.rect(screen, BG2, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
            if col == SQUARES - 1:
                continue
            counter += 1

def draw_scoreboard(screen, score_value, x, y):
    font = pygame.font.Font("freesansbold.ttf", 32)
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def spawn_food(screen, x, y):
    pygame.draw.rect(screen, "red", [(x, y), (PIXELS, PIXELS)])
    

# Game Program Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Draw the background     
    draw_background(screen)
    
    #Head of snake drawn
    snake.snake_draw(PIXELS, screen)
    
    #Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and snake.current_direction != "s":
        snake.player_vel_x = 0
        snake.player_vel_y = -snake.movement_speed * dt
        snake.current_direction = "w"
    if keys[pygame.K_s] and snake.current_direction != "w":
        snake.player_vel_x = 0
        snake.player_vel_y = snake.movement_speed * dt
        snake.current_direction = "s"
    if keys[pygame.K_a] and snake.current_direction != "d":
        snake.player_vel_y = 0
        snake.player_vel_x = -snake.movement_speed * dt
        snake.current_direction = "a"
    if keys[pygame.K_d] and snake.current_direction != "a":
        snake.player_vel_y = 0
        snake.player_vel_x = snake.movement_speed * dt
        snake.current_direction = "d"
        
    snake.player_pos_x += snake.player_vel_x 
    snake.player_pos_y += snake.player_vel_y 
    
    snake.snake_update()
    
    #Boundaries
    if snake.player_pos_x <= 0:
        snake.player_pos_x = 0
    elif snake.player_pos_x >= WIDTH - PIXELS:
        snake.player_pos_x = WIDTH - PIXELS

    if snake.player_pos_y <= 0:
        snake.player_pos_y = 0
    elif snake.player_pos_y >= HEIGHT - PIXELS:
        snake.player_pos_y = HEIGHT - PIXELS
        
    #Food Handling
    spawn_food(screen, food_pos_x, food_pos_y)   
    distance_head_food = math.sqrt(pow(food_pos_x - snake.player_pos_x, 2) + pow(food_pos_y - snake.player_pos_y, 2))
    if distance_head_food < PIXELS:
        score_value += 1
        snake.snake_body.append(snake.snake_directional())
        draw_background(screen)
        food_pos_x , food_pos_y = get_food_pos(snake.snake_body)
       
        spawn_food(screen, food_pos_x, food_pos_y)

    draw_scoreboard(screen, score_value, scoreboard_x_coord, scoreboard_y_coord)

    pygame.display.flip()
    
    dt = clock.tick(30) / 1000

pygame.quit()