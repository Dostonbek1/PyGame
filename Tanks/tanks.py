######################################################################
# Author: Dostonbek Toirov
#
# Project: Tanks
# Purpose: To create a simple tank game using pygame
#
######################################################################
# Acknowledgements: Harrison, Aleksandr Krasnov
#
####################################################################################

# Imports
import pygame
import random

# Initializing pygame
pygame.init()

# Setting the the sizes of the game frame
display_width = 800
display_height = 600

# Creating the game frame
gameDisplay = pygame.display.set_mode((display_width, display_height))

# Sounds
fire_sound = pygame.mixer.Sound("boom.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Setting the caption of the game
pygame.display.set_caption('Tanks')

# Setting the icon of the game
icon = pygame.image.load('tanks.png')
pygame.display.set_icon(icon)

# Colors
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)
clock = pygame.time.Clock()

# Tank size
tankWidth = 40
tankHeight = 20

# Tank's turret size
turretWidth = 5

# Tank's wheel size
wheelWidth = 5

# Ground size
ground_height = 35

# Fonts
smallfont = pygame.font.SysFont("comicsansms", 30)
btn = pygame.font.Font("euphoric.ttf", 25)
largefont = pygame.font.Font("SEGA.TTF", 65)


##### Functions #####

def game_intro():
    '''
    Creating the intro window of the game
    :return:
    '''
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Tanks",green,-100,size="large")
        message_to_screen("The objective is to shoot and destroy",black, 0, size="small")
        message_to_screen("the enemy tank before they destroy you.",black,40)
        message_to_screen("The more enemies you destroy, the harder they get.",black,80)

        button("play",150,500,100,50,green,light_green,action="play")
        button("controls",350,500,100,50,yellow,light_yellow,action="controls")
        button("quit",550,500,100,50,red,light_red,action="quit")

        pygame.display.update()

        clock.tick(15)


def text_objects(text, color, size="small"):
    '''
    Given the certain parameters, sets the font and the color
    of the text
    :param text:
    :param color:
    :param size:
    :return:
    '''
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "button":
        textSurface = btn.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def button(text, x, y, width, height, inactive_color, active_color, action=None):
    '''
    Creating the buttons
    :param text:
    :param x:
    :param y:
    :param width:
    :param height:
    :param inactive_color:
    :param active_color:
    :param action:
    :return:
    '''
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "controls":
                game_controls()

            if action == "play":
                gameLoop()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text, black, x, y, width, height)                        # Call to text_to_button() function


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="button"):
    '''
    Writing the texts for the buttons on the screen
    :param msg:
    :param color:
    :param buttonx:
    :param buttony:
    :param buttonwidth:
    :param buttonheight:
    :param size:
    :return:
    '''
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    gameDisplay.blit(textSurf, textRect)


def message_to_screen(msg, color, y_displace=0, size="small"):
    '''
    Given the corresponding color, text, and coordinates, writes a text on
    the screen
    :param msg:
    :param color:
    :param y_displace:
    :param size:
    :return:
    '''
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)


def tank(x,y, turPos):
    '''
    Creating tank objects
    :param x:
    :param y:
    :param turPos:
    :return:
    '''
    x = int(x)
    y = int(y)

    possibleTurrets = [(x-27, y-2),
                       (x-26, y-5),
                       (x-25, y-8),
                       (x-23, y-12),
                       (x-20, y-14),
                       (x-18, y-15),
                       (x-15, y-17),
                       (x-13, y-19),
                       (x-11, y-21)
                       ]

    pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))                    # head of the tank
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))      # body of the tank
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)   # turret (nose) of the tank

    startX = 21
    for i in range(7):
        pygame.draw.circle(gameDisplay,black, (x-startX, y+20), wheelWidth)             # wheels of the tank
        startX -= 7

    return possibleTurrets[turPos]                                                      # returns the turret position

def enemy_tank(x,y, turPos):
    '''
    Creating the enemy tank
    :param x:
    :param y:
    :param turPos:
    :return:
    '''
    x = int(x)
    y = int(y)

    possibleTurrets = [(x+27, y-2),
                       (x+26, y-5),
                       (x+25, y-8),
                       (x+23, y-12),
                       (x+20, y-14),
                       (x+18, y-15),
                       (x+15, y-17),
                       (x+13, y-19),
                       (x+11, y-21)
                       ]

    pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))                    # head of the enemy tank
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))      # body of the enemy tank
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)   # turret (nose) of the enemy tank

    startX = 21
    for i in range(7):
        pygame.draw.circle(gameDisplay,black, (x-startX, y+20), wheelWidth)             # wheels of the enemy tank
        startX -= 7

    return possibleTurrets[turPos]                                                      # returns the turret position


def game_controls():
    '''
    Drawing a window of controls where it describes the keys to be used
    in the game
    :return:
    '''
    gcont = True

    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("Controls",green,-100,size="large")
        message_to_screen("Fire: Spacebar",black,-30)
        message_to_screen("Move Turret: Up and Down arrows",black,10)
        message_to_screen("Move Tank: Left and Right arrows",black,50)
        message_to_screen("Level of Power: A - Less; D - More",black,90)
        message_to_screen("Pause: P",black,130)


        button("play",150,500,100,50,green,light_green,action="play")
        button("quit",550,500,100,50,red,light_red,action="quit")

        pygame.display.update()
        clock.tick(15)


def pause():
    '''
    Pauses the game
    :return:
    '''
    paused = True

    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue playing or Q to quit",black,25)

    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)


def barrier(xlocation,randomHeight, barrier_width):
    '''
    Draws a barrier in random between two tanks
    :param xlocation:
    :param randomHeight:
    :param barrier_width:
    :return:
    '''
    pygame.draw.rect(gameDisplay, black, [xlocation, display_height-randomHeight, barrier_width, randomHeight] )


def explosion(x, y, size=50):
    '''
    Draws the scene of an explosion when a shell hits an object
    :param x:
    :param y:
    :param size:
    :return:
    '''
    pygame.mixer.Sound.play(explosion_sound)
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startPoint = x,y

        colorChoices = [red, light_red, yellow, light_yellow]
        magnitude = 1

        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1 * magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)

            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)

        explode = False

def fireShell(xy,tankx,tanky,turPos,gun_power,xlocation,barrier_width,randomHeight,enemyTankX,enemyTankY):
    '''
    The action of the player tank's shell, once it is released.
    Draws parabola-like graph to simulate the shell direction
    :param xy:
    :param tankx:
    :param tanky:
    :param turPos:
    :param gun_power:
    :param xlocation:
    :param barrier_width:
    :param randomHeight:
    :param enemyTankX:
    :param enemyTankY:
    :return:
    '''
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    damage = 0

    startingShell = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, green, (startingShell[0],startingShell[1]),5)

        startingShell[0] -= (12 - turPos) * 2
        startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPos + turPos / (12 - turPos)))

        if startingShell[1] > display_height - ground_height:
            hit_x = int((startingShell[0] * display_height - ground_height) / startingShell[1])
            hit_y = int(display_height - ground_height)                                             # Shell impact at x and y

            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                damage = 25                                                                         # Critical Hit
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                damage = 18                                                                         # Hard Hit
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                damage = 10                                                                         # Medium Hit
            elif enemyTankX + 35 > hit_x > enemyTankX - 35:
                damage = 5                                                                          # Light Hit

            explosion(hit_x, hit_y)                                                                 # Call to an explosion function, and draws explosion
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            explosion(hit_x, hit_y)
            fire = False

        pygame.display.update()
        clock.tick(100)

    return damage

def e_fireShell(xy,tankx,tanky,turPos,gun_power,xlocation,barrier_width,randomHeight,pTankX,pTankY):
    '''
    The action of the enemy tank's shell, once it is released.
    Draws parabola-like graph to simulate the shell direction
    :param xy:
    :param tankx:
    :param tanky:
    :param turPos:
    :param gun_power:
    :param xlocation:
    :param barrier_width:
    :param randomHeight:
    :param pTankX:
    :param pTankY:
    :return:
    '''
    pygame.mixer.Sound.play(fire_sound)         # sound of fire
    damage = 0                                  # initial valur of damage

    currentPower = 1
    power_found = False

    while not power_found:
        currentPower += 1
        if currentPower > 100:
            power_found = True

        fire = True
        startingShell = list(xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            startingShell[0] += (12 - turPos) * 2
            startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015 / (currentPower / 50)) ** 2) - (turPos + turPos / (12 - turPos)))

            if startingShell[1] > display_height - ground_height:
                hit_x = int((startingShell[0] * display_height - ground_height) / startingShell[1])
                hit_y = int(display_height - ground_height)
                if pTankX + 15 > hit_x > pTankX - 15:
                    power_found = True
                fire = False

            check_x_1 = startingShell[0] <= xlocation + barrier_width
            check_x_2 = startingShell[0] >= xlocation

            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(startingShell[0])
                hit_y = int(startingShell[1])
                fire = False

    fire = True
    startingShell = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, green, (startingShell[0],startingShell[1]),5)

        startingShell[0] += (12 - turPos) * 2

        gun_power = random.randrange(int(currentPower * 0.99), int(currentPower * 1.01))

        startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPos + turPos / (12 - turPos)))

        if startingShell[1] > display_height - ground_height:
            hit_x = int((startingShell[0] * display_height - ground_height) / startingShell[1])
            hit_y = int(display_height - ground_height)

            if pTankX + 10 > hit_x > pTankX - 10:
                damage = 25                             # Critical Hit
            elif pTankX + 15 > hit_x > pTankX - 15:
                damage = 18                             # Hard Hit
            elif pTankX + 25 > hit_x > pTankX - 25:
                damage = 10                             # Medium Hit
            elif pTankX + 35 > hit_x > pTankX - 35:
                damage = 5                              # Light Hit

            explosion(hit_x, hit_y)                     # call to an explosion() function
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:             # barrier impact
            hit_x = int(startingShell[0])           # Impact at x
            hit_y = int(startingShell[1])           # Impact at y
            explosion(hit_x, hit_y)
            fire = False

        pygame.display.update()
        clock.tick(100)

    return damage


def power(level):
    '''
    Diplays the level of power of the tank shell
    :param level:
    :return:
    '''
    text = smallfont.render("Power: " + str(level) + "%", True, black)
    gameDisplay.blit(text, [display_width / 2, 0])


def health_bars(player_health, enemy_health):
    '''
    Creating bars that show the health level of both players
    :param player_health:
    :param enemy_health:
    :return:
    '''
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))


def game_over():
    '''
    Creating game over window of the game
    Called when the player loses the game
    :return:
    '''
    game_over = True

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("Game Over",green,-100,size="large")
        message_to_screen("You died!",black,-30)

        button("play again",150,500,150,50,green,light_green,action="play")
        button("controls",350,500,150,50,yellow,light_yellow,action="controls")
        button("quit",550,500,150,50,red,light_red,action="quit")

        pygame.display.update()
        clock.tick(15)


def you_win():
    '''
    The window of the game that shows that the player has
    won the game. Called when the player wins the game
    :return:
    '''
    win = True

    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("You won",green,-100,size="large")
        message_to_screen("Congratulations!",black,-30)

        button("play again",150,500,150,50,green,light_green,action="play")
        button("controls",350,500,150,50,yellow,light_yellow,action="controls")
        button("quit",550,500,150,50,red,light_red,action="quit")

        pygame.display.update()
        clock.tick(15)


def gameLoop():
    '''
    The body of the game, where the main game actions take place,
    and where all the functions are called
    :return:
    '''
    gameExit = False
    gameOver = False
    FPS = 15

    mainTankX = display_width * 0.9         # player's tank position (x coordinate)
    mainTankY = display_height * 0.9        # player's tank position (y coordinate)
    tankMove = 0
    currentTurPos = 0
    changeTur = 0

    enemyTankX = display_width * 0.1        # enemy tank position (x coordinate)
    enemyTankY = display_height * 0.9       # enemy tank position (y coordinate)

    xlocation = (display_width/2) + random.randint(-0.1*display_width, 0.1*display_width)
    randomHeight = random.randrange(display_height*0.1,display_height*0.6)
    barrier_width = 50

    fire_power = 50
    power_change = 0

    player_health = 100
    enemy_health = 100

    while not gameExit:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove = -5

                elif event.key == pygame.K_RIGHT:
                    tankMove = 5

                elif event.key == pygame.K_UP:
                    changeTur = 1

                elif event.key == pygame.K_DOWN:
                    changeTur = -1

                elif event.key == pygame.K_p:
                    pause()

                elif event.key == pygame.K_SPACE:
                    damage = fireShell(gun,mainTankX,mainTankY,currentTurPos,fire_power,xlocation,barrier_width,randomHeight,enemyTankX,enemyTankY)
                    enemy_health -= damage
                    if enemy_health < 0:
                        enemy_health = 0

                    possibleMovement = ['f','r']
                    moveIndex = random.randrange(0,2)

                    for x in range(random.randrange(0,10)):
                        if display_width * 0.3 > enemyTankX > display_width * 0.03:
                            if possibleMovement[moveIndex] == "f":
                                enemyTankX += 5
                            elif possibleMovement[moveIndex] == "r":
                                enemyTankX -= 5

                            gameDisplay.fill(white)
                            health_bars(player_health, enemy_health)
                            gun = tank(mainTankX,mainTankY,currentTurPos)
                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
                            fire_power += power_change

                            power(fire_power)

                            barrier(xlocation,randomHeight,barrier_width)
                            gameDisplay.fill(green, rect=[0, display_height - ground_height, display_width, display_height])
                            pygame.display.update()

                            clock.tick(FPS)

                    damage = e_fireShell(enemy_gun,enemyTankX,enemyTankY,8,50,xlocation,barrier_width,randomHeight,mainTankX,mainTankY)
                    player_health -= damage
                    if player_health < 0:
                        player_health = 0

                elif event.key == pygame.K_a:
                    power_change = -1

                elif event.key == pygame.K_d:
                    power_change = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0

        mainTankX += tankMove
        currentTurPos += changeTur

        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0

        if mainTankX - (tankWidth / 2) < xlocation + barrier_width:
            mainTankX += 5

        gameDisplay.fill(white)
        health_bars(player_health, enemy_health)
        gun = tank(mainTankX,mainTankY,currentTurPos)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)

        fire_power += power_change
        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1
        power(fire_power)

        barrier(xlocation,randomHeight,barrier_width)
        gameDisplay.fill(green, rect=[0, display_height - ground_height, display_width, display_height])
        pygame.display.update()

        if player_health == 0:
            game_over()
        elif enemy_health == 0:
            you_win()

        clock.tick(FPS)

    pygame.quit()
    quit()


def main():
    game_intro()
    gameLoop()


if __name__ == '__main__':
    main()
