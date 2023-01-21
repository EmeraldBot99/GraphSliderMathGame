import pygame
import math
import time
import random

#question arrays (pain)
questions = [
'7 x 8', '42 ÷ 7', '9 x 4', '6 x 9', '20 x 17', '6 x __ = 72', '425 ÷ 10', '350 ÷ 5', '98 ÷ __ = 14', 'sin(2π)'   
]

answers = [
    [56,64,48],[6,5,7],[36,40,32],[54,63,53],[340,357,327],[12,11,13],[42.5,42,43],[ 70,75,65],[7,14,6],[0,'π',2.28]    

]

# Initialize Pygame
pygame.init()

# Set screen size
size = (800, 600)
screen = pygame.display.set_mode(size)

# Set up game variables
done = False
clock = pygame.time.Clock()

# Choose a mathematical equation
equation = lambda x: int(math.sin(x/640*4*math.pi)*50+240)

# initial variables
player_x = 240
player_y = equation(player_x)
player_speed = 2.2
scroll_x = 0
player_vy = 0
player_vx = 0
gravity = 0.5
on_ground = True
jump_cooldown = 0
jump_cooldown_time = 10
object_x = random.randrange(player_x+scroll_x, scroll_x+size[0])
font = pygame.font.SysFont('freesansbold.ttf',32)
question = 0 
answer = random.randrange(0,len(answers[question]))

# Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Check if the spacebar is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if on_ground and jump_cooldown == 0:
            player_vy = -8  # Apply an upward force when the spacebar is pressed
 
            on_ground = False
            jump_cooldown += 4

    # Update the player's vertical velocity
    player_vy += gravity

    # Update the player's position
    player_y += player_vy
    player_x += player_vx
    
    if player_x > 240:
        player_x -= 0.5

    # Check if the player is on the graph
    if player_y > equation(player_x+scroll_x):
        player_y = equation(player_x+scroll_x)
        player_vy = 0
        on_ground = True
        player_vx = 0
    
    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the graph of the equation
    for x in range(size[0]):
        y = equation(x + scroll_x)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 1)

    # Draw the player
    pygame.draw.circle(screen, (255, 0, 0), (player_x, player_y), 10)

    

    #check if player has 'collected' an answer
    if player_x >= object_x-10 and player_x <= object_x+10:
        if player_y <= equation(object_x+scroll_x)+10 and player_y >= equation(object_x+scroll_x)-10:
            #handle answer logic
            object_x = random.randrange(round(player_x+50), size[0])
            if answer == 0:
                question += 1
            else:
                done = True
            answer = random.randrange(0,len(answers[question]))
            
    #if answer position outside of screen; generate a new one
    if object_x <= 0:
        object_x = random.randrange(400,size[0])
        answer = random.randrange(0,len(answers[question]))
    
    
    #draw answer to screen
    pygame.draw.circle(screen,(40,40,40),(object_x+10, equation(object_x+10+scroll_x)),10)
    
    
    #render text
    questiontext = font.render(str(questions[question]),True,(0,0,0),)
    screen.blit(questiontext,(400-len(questions[question]*10),400))
    
    answertext = font.render(str(answers[question][answer]),False,(255,0,255))
    screen.blit(answertext,(object_x,100))

    
    #move answer closer to player
    object_x -= 3

    #update scroll
    scroll_x += player_speed

    #update jump cooldown
    if jump_cooldown > 0:
        jump_cooldown -= 1
    
    # Update the screen
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

# Exit Pygame
pygame.quit()
