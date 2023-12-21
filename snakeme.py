import sys
import pygame
import random
import time

pygame.init()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

width = 600
height = 600

TIMER = 10
speed = 10
SNAKE_SIZE = 20
GRID_SIZE = 20
FONT = pygame.font.Font(None, 36)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def generate_food(snake):
    while True:
        food = (random.randint(0, (width - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (height - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
        if food not in snake:
            return food

def draw_snake(display, snake):
    for segment in snake:
        pygame.draw.rect(display, GREEN, (*segment, SNAKE_SIZE, SNAKE_SIZE))

def draw_food(display, food):
    pygame.draw.rect(display, RED, (*food, SNAKE_SIZE, SNAKE_SIZE))

def draw_timer(display, timer_value):
    text = FONT.render(f"Timer: {round(timer_value)}s", True, WHITE)
    display.blit(text, (10, 10))

def draw_score(display, score):
    text = FONT.render(f"Count: {score}", True, WHITE)
    display.blit(text, (width - 200, 10))

def check_move(snake):
    head = snake[0]
    return head in snake[1:] or (
        head[0] < 0 or head[0] >= width or
        head[1] < 0 or head[1] >= height
    )

def handle_input(snake, direction, game_started, count, speed):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != DOWN:
        return UP, True, count, speed
    elif keys[pygame.K_DOWN] and direction != UP:
        return DOWN, True, count, speed
    elif keys[pygame.K_LEFT] and direction != RIGHT:
        return LEFT, True, count, speed
    elif keys[pygame.K_RIGHT] and direction != LEFT:
        return RIGHT, True, count, speed
    elif keys[pygame.K_SPACE] and game_started and count != 0:
        snake.pop()
        count -= 1
        speed -= 1
        return direction, True, count, speed
    return direction, game_started, count, speed

def update(snake, direction, food, food_timer_start, game_started, count, score, speed):
    if not game_started:
        return False, snake, food, food_timer_start, count, score, speed

    head = (snake[0][0] + direction[0] * GRID_SIZE, snake[0][1] + direction[1] * GRID_SIZE)
    snake.insert(0, head)

    if head == food:
        food = generate_food(snake)
        food_timer_start = time.time()
        count += 1
        score += 1
        speed += 0.5
    else:
        snake.pop()


    timer_value = TIMER - (time.time() - food_timer_start)
    if timer_value <= 0 or check_move(snake):
        return True, snake, food, food_timer_start, count, score, speed

    return False, snake, food, food_timer_start, count, score, speed

def instructions_prompt(display):
    display.fill(BLACK)
    instr_text1 = FONT.render("Welcome to Snake!", True, WHITE)
    instr_text2 = FONT.render("Eat as many of the red foods as you can!", True, WHITE)
    instr_text3 = FONT.render("The more you eat, the faster you get!", True, WHITE)
    instr_text4 = FONT.render("Press 'space' to decrease the size of", True, WHITE)
    instr_text4cont = FONT.render("your snake and slow your speed!", True, WHITE)
    instr_text5 = FONT.render("If you don't eat a food, run into yourself,", True, WHITE)
    instr_text5cont = FONT.render("or run into a wall, you lose!", True, WHITE)
    instr_text6 = FONT.render("Press any key to start the game!", True, WHITE)
    display.blit(instr_text1, (width / 6, height / 8))
    display.blit(instr_text2, (width / 6, height / 8 + 50))
    display.blit(instr_text3, (width / 6, height / 8 + 100))
    display.blit(instr_text4, (width / 6, height / 8 + 150))
    display.blit(instr_text4cont, (width / 6, height / 8 + 200))
    display.blit(instr_text5, (width / 6, height / 8 + 250))
    display.blit(instr_text5cont, (width / 6, height / 8 + 300))
    display.blit(instr_text6, (width / 6, height / 8 + 350))
    pygame.display.flip()

def game_over_prompt(display, score):
    display.fill(BLACK)
    gg_text = FONT.render(f"Game Over! Score: {score}", True, WHITE)
    quit_text = FONT.render("Press 'q' to quit", True, WHITE)
    cont_text = FONT.render("'Enter' to continue", True, WHITE)

    display.blit(gg_text,  (width / 6, height / 3))
    display.blit(quit_text,  ((width / 6), (height / 3) + 50))
    display.blit(cont_text,  ((width / 6), (height / 3) + 100))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return False
                elif event.key == pygame.K_q:
                    return True

def main():
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = RIGHT
    food = generate_food(snake)
    game_started = False
    first_run = True
    count = 0
    score = 0
    speed = 10

    clock = pygame.time.Clock()
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    while first_run:
        instructions_prompt(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                first_run = False
    
    food_timer_start = time.time()

    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        direction, game_started, count, speed = handle_input(snake, direction, game_started, count, speed)
        game_over, snake, food, food_timer_start, count, score, speed= update(snake, direction, food, 
                                                    food_timer_start, game_started, count, score, speed)

        display.fill(BLACK)
        draw_snake(display, snake)
        draw_food(display, food)
        draw_timer(display, TIMER - (time.time() - food_timer_start))
        draw_score(display, score)
        pygame.display.flip()

        if game_over:
                if game_over_prompt(display, score):
                    pygame.quit()
                    sys.exit()
                else:
                    main()

        clock.tick(speed)

main()
