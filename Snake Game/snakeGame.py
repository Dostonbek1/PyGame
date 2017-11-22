# Snake Game!
# by Dostonbek Toirov

# game imports
import pygame, sys, random, time

# Play Area
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption("Snake Game!")

# Colors
red = pygame.Color("red")     # used for gameover 
green = pygame.Color("green") # used for snake
black = pygame.Color("black") # used for score
white = pygame.Color("white") # used for background
brown = pygame.Color("brown") # used for food


# FPS controller
fpsController = pygame.time.Clock()

# Important variables
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]


foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
foodSpawn = True

direction = 'RIGHT'
changeTo = direction

# Game over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 15)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit() # pygame exit
    sys.exit() # console
score = 0

# Function that shows score
def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 24)
    Ssurf = sFont.render('Score : {0}'.format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 120)
    playSurface.blit(Ssurf, Srect)


# Main Logic of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validation of direction
    if changeTo == "RIGHT" and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeTo == "LEFT" and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeTo == "UP" and not direction == 'DOWN':
        direction = 'UP'
    if changeTo == "DOWN" and not direction == 'UP':
        direction = 'DOWN'

    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10


    # Snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    # Food Spawn
    if foodSpawn == False:
        foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
    foodSpawn = True

    playSurface.fill(white)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1],10,10))

    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1],10,10))
    
    # Get rid of walls
    if snakePos[0] < 0:
        snakePos[0] = 710
    if snakePos[0] > 710:
        snakePos[0] = 0
    if snakePos[1] < 0:
        snakePos[1] = 450
    if snakePos[1] > 450:
        snakePos[1] = 0

    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]: 
            gameOver()

    showScore()
    pygame.display.flip()
    fpsController.tick(17)

