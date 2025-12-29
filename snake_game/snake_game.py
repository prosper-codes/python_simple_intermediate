import pygame
import random
#Initialize pygame
pygame.init()
 
# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")
 
# Create a boolean value to see if game is running
game_over = False
score=0
#Create a colour
white =(255,255,255)
black=(0,0,0)
red=(255,0,0)
 
#setting co-ordinates for snake
#Center cordinates
x1 = window_width / 2
y1 = window_height / 2
 
#change in x and y
x1_change = 0
y1_change = 0
 
snake_block = 10
snake_speed= 15
 
snake_body=[]
length_of_snake=1
 
#create a clock
clock = pygame.time.Clock()
 
 # Set up the initial position of the food
foodx = round(random.randrange(
        0, window_width - snake_block) / 10.0) * 10.0
foody = round(random.randrange(
        0, window_height - snake_block) / 10.0) * 10.0
 
 
 
while not game_over:
    # Check for events such as keypress
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = snake_block
                x1_change = 0
            
    x1+=x1_change
    y1+=y1_change
    
    
    # Check if the snake hits the boundary of the game window
    if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
        game_over = True
            
            
    window.fill(black
                 )
    pygame.draw.rect(window, red, [foodx,foody,snake_block,snake_block])
    
    #update the snake's body
    snake_head=[]
    snake_head.append(x1)
    snake_head.append(y1)
    snake_body.append(snake_head)
    
    if len(snake_body)>length_of_snake:
        del snake_body[0]
    
    #Check if snake hits itself
    for segment in snake_body[:-1]:
        if segment == snake_head:
            game_over=True
    
    #Drawing the snake
    for segment in snake_body:
        pygame.draw.rect(window,white,[segment[0],segment[1],snake_block,snake_block])
    
    #show score code
    font_style = pygame.font.SysFont(None, 50)
    score_text = font_style.render("Score: "+str(score),True,white)
    window.blit(score_text, (10,10))
    pygame.display.update()
    
    if x1 == foodx and y1 == foody:
        # if this happens, recalculate food's position & update score
        foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
        length_of_snake+=1
        score+=1
    clock.tick(30)