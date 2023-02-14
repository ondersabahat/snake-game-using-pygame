"""
 A simple retro snake game: 

 This is my first game code with using pygame 

"""

import pygame, sys, random
from pygame import Vector2

# initialize pygame 
pygame.init()

# color variables
BACKGROUND = (32, 32, 32)
SNAKE = (173, 204, 96)

# divide screen 25x25 cells to get 625 x 625 pixels window 
CELL_SIZE = 25 
NUMBER_OF_CELLS = 25

# offset from main game window 
OFFSET = 75

# font variables 
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 50)

# the main game window 
WIDTH, HEIGHT = ((2 * OFFSET + CELL_SIZE * NUMBER_OF_CELLS), (2 * OFFSET + CELL_SIZE * NUMBER_OF_CELLS)) 
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# using Clock object to set game speed 60 FPS for all users
FPS = 60
clock = pygame.time.Clock()

# food object 
class Food: 
    def __init__(self, snake_body): 
        self.position = self.generate_position(snake_body)

    def draw(self): 
        rect = pygame.Rect(OFFSET + self.position.x * CELL_SIZE, OFFSET + self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        window.blit(food_surface, rect)

    def generate_random_cell(self):
        x = random.randint(0, NUMBER_OF_CELLS-1)
        y = random.randint(0, NUMBER_OF_CELLS-1)
        return Vector2(x, y)

    # when the snake eats food, position of food will be renewed
    def generate_position(self, snake_body):        
        position = self.generate_random_cell() 
        while position in snake_body:
            position = self.generate_random_cell()    
        return position


# snake object 
class Snake: 
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_section = False
        self.eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
        self.wall_sound = pygame.mixer.Sound("Sounds/wall.mp3")
    
    def draw(self):
        for section in self.body:
            section_rect = (OFFSET + section.x * CELL_SIZE, OFFSET + section.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, SNAKE, section_rect, 0, 9)
    
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_section:
            self.add_section = False
        else:
            self.body = self.body[:-1]

    # reset snake to beginning position and size
    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

# main game object that contains all elements 
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "PLAY"
        self.score = 0

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state == "PLAY":
            self.snake.update()
            self.check_collision_food()
            self.check_collision_borders()
            self.check_collision_tail()
      
    # when the snake eats foods
    def check_collision_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_position(self.snake.body)
            self.snake.add_section = True
            self.score += 1
            self.snake.eat_sound.play()

    def check_collision_borders(self):
        if self.snake.body[0].x == NUMBER_OF_CELLS or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == NUMBER_OF_CELLS or self.snake.body[0].y == -1:
            self.game_over()

    def check_collision_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_position(self.snake.body)
        self.state = "GAMEOVER"
        self.score = 0
        self.snake.wall_sound.play()

game = Game()
food_surface = pygame.image.load("Graphics/apple.png")

# maintaining the snake's speed -- faster number upper 160, slower number below 160 
snake_update = pygame.USEREVENT
pygame.time.set_timer(snake_update, 160)

# game loop 
while True:

    for event in pygame.event.get():
        if event.type == snake_update:
            game.update()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        # user controls 
        if event.type == pygame.KEYDOWN:
            if game.state == "GAMEOVER": # if user press a key restart game 
                game.state = "PLAY"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # draw
    window.fill(BACKGROUND) # background color 
    pygame.draw.rect(window, SNAKE, (OFFSET - 5, OFFSET - 5, CELL_SIZE * NUMBER_OF_CELLS + 10,  CELL_SIZE * NUMBER_OF_CELLS + 10), 5) # 5 pixel black border
    game.draw()
    title = title_font.render("Snake Game", True, SNAKE)
    window.blit(title, (OFFSET-5, 20))
    score = title_font.render(("Score: " + str(game.score)), True, SNAKE)
    window.blit(score, (CELL_SIZE * NUMBER_OF_CELLS - OFFSET, 20))


    pygame.display.update()
    clock.tick(FPS)


