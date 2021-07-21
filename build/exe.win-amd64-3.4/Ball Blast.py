import pygame
import time
import random

pygame.init()

white = (255,255,255)
red = (200,0,0)
light_red = (255,0,0)
black = (0,0,0)
green = (34,177,76)
yellow = (200,200,0)
light_yellow = (255,255,0)
blue = (0,0,255)
light_blue = (0,162,232)
light_green = (0,255,0)

width = 800
height = 600

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ball Blast")

#icon = pygame.image.load('Apple.png')
#pygame.display.set_icon(icon)

#img = pygame.image.load('snakehead.png')
bulletimg = pygame.image.load('bullet.png')

FPS = 20
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 42)
largefont = pygame.font.SysFont("comicsansms", 70)

clock = pygame.time.Clock()
colours = [red,light_red,yellow,light_yellow,blue,light_blue,green,light_green]
tankWidth = 40
tankHeight = 20
wheelWidth = 5
turretWidth = 5
ground_height = 35
projectile_width = 31
projectile_colour = colours[random.randint(0,7)]
bullet_state = "ready"

def pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pause = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        message("Paused", black, -100, size = "large")
        message("Press C to continue and Q to quit", black, 25)
        pygame.display.update()
        clock.tick(20)

def score(score):
    text = smallfont.render("Score: " + str(score) , True, black)
    gameDisplay.blit(text, (0,0))

def text_objects(text,colour,size):
    if size == "small":
        textSurface = smallfont.render(text, True, colour)
    if size == "medium":
        textSurface = medfont.render(text, True, colour)
    if size == "large":
        textSurface = largefont.render(text, True, colour)
        
    return textSurface, textSurface.get_rect()

def message(msg,colour,displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,colour,size)
    textRect.center = (width/2),(height/2) + displace
    gameDisplay.blit(textSurf, textRect)

def text_to_button(msg, colour, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,colour,size)
    textRect.center = ((buttonx+(buttonwidth/2),buttony+(buttonheight/2)))
    gameDisplay.blit(textSurf, textRect)
            
def game_controls():
    gcont = True
    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        message("Controls", green, -100, "large")
        message("Fire: Spacebar", black, -30)
        #message("Move Turret: Up and Down arrows", black, 10)
        message("Move Tank: Left and Right arrows", black, 10)
        message("Pause: P", black, 50)
        #message("Adjust Power: A and D", black, 90)
        button("Play",150,500,100,50,light_green,green,action="play")
        button("Main Menu",350,500,100,50,light_yellow,yellow,action="main")
        button("Quit",550,500,100,50,light_red,red,action="quit")
        pygame.display.update()
        clock.tick(20)

def button(text,x,y,width,height,inactive_colour,active_colour,action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_colour, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "main":
                intro()
            if action == "credits":
                credit()
    else:
        pygame.draw.rect(gameDisplay, inactive_colour, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)

def credit():
    c = True
    while c:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        font = pygame.font.SysFont('comicsansms',40)
        text = font.render("Made by Aryav Tiwari",True,black)
        gameDisplay.blit(text, ((width/2) - (text.get_width()/2),(height/2) - (text.get_height()/2)))
        button("Play",150,500,100,50,light_green,green,action="play")
        button("Controls",350,500,100,50,light_yellow,yellow,action="controls")
        button("Quit",550,500,100,50,light_red,red,action="quit")
        pygame.display.update()
        clock.tick(20)

def tank(x,y):
    x = int(x)
    y = int(y)
    pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x - tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x, y), (x, y - 25), turretWidth)
    pygame.draw.circle(gameDisplay, black, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x - 10, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x - 5, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x + 5, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x + 10, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x + 15, y + 20), wheelWidth)

visible = "t"
def projectile(x,y,life):
    visible = "t"
    font = pygame.font.SysFont('comicsansms',20)
    life = int(life)
    x = int(x)
    y = int(y)
    pygame.draw.circle(gameDisplay, projectile_colour, (x,y), projectile_width)
    text = font.render(str(life),True,white)
    gameDisplay.blit(text, (x - (text.get_width()/2),y - (text.get_height()/2)))

visibleshoot = True
def shoot(x,y):
    global bullet_state
    global visibleshoot
    bullet_state = "fire"
    gameDisplay.blit(bulletimg, (x - 10, y - 20))

def intro():
    gameIntro = True
    while gameIntro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        message("Welcome To Ball Blast!", green, -100, "large")
        message("The objective is to shoot and destroy", black, -30)
        message("the balls before they destroy you.", black, 10)
        message("The more balls you destroy, the harder the game get.", black, 50)
        #message("Press C to play, P to pause and Q to quit", black, 180)
        button("Play",150,500,100,50,light_green,green,action="play")
        button("Controls",350,500,100,50,light_yellow,yellow,action="controls")
        button("Quit",550,500,100,50,light_red,red,action="quit")
        button("Credits",350,420,100,50,light_blue,blue,action="credits")
        pygame.display.update()
        clock.tick(20)

def over():
    gameOver = True
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        message("Game Over!", red, -100, "large")
        message("You died", black, -30)
        #message("the enemy tank before they destroy you.", black, 10)
        #message("The more enemies you destroy, the harder they get.", black, 50)
        #message("Press C to play, P to pause and Q to quit", black, 180)
        button("Replay",150,500,100,50,light_green,green,action="play")
        #button("Controls",350,500,100,50,light_yellow,yellow,action="controls")
        button("Quit",550,500,100,50,light_red,red,action="quit")
        pygame.display.update()
        clock.tick(20)

def win():
    win = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        message("Win!", green, -100, "large")
        message("Congratulation!", black, -30)
        message("When are you throwing up a party?", black, 10)
        #message("The more enemies you destroy, the harder they get.", black, 50)
        #message("Press C to play, P to pause and Q to quit", black, 180)
        button("Replay",150,500,100,50,light_green,green,action="play")
        #button("Controls",350,500,100,50,light_yellow,yellow,action="controls")
        button("Quit",550,500,100,50,light_red,red,action="quit")
        pygame.display.update()
        clock.tick(20)
        
def gameLoop():
    global bullet_state
    global visibleshoot
    global visible
    mainTankX = width * 0.9
    mainTankY = height * 0.9
    shooty = int(mainTankY)
    shootx = int(mainTankX)
    gameExit = False
    gameOver = False
    tankMove = 0
    projectilex = width - 35
    projectiley = height * 0.1
    speed = 10
    one = -5
    life = random.randint(250,2000)

    while not gameExit:
             
        while gameOver == True:
            gameDisplay.fill(white)
            message("Game Over", red, -50, size = "large")
            message("Press C to play again or press Q to quit", black, 50, size = "medium")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        gameDisplay.fill(light_blue)
        gameDisplay.fill(green, rect=[0,height-ground_height,width,ground_height])
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove = -20
                elif event.key == pygame.K_RIGHT:
                    tankMove = 20
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    shoot(mainTankX, shooty)
                    bullet_state = "fire"
                elif event.key == pygame.K_a:
                    pass
                elif event.key == pygame.K_d:
                    pass
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                    tankMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pass
                if event.key == pygame.K_SPACE:
                    pass
        
        mainTankX += tankMove
        if mainTankX >= width - 20:
            mainTankX = width - 20
        elif mainTankX <= 20:
            mainTankX = 20
        tank(mainTankX,mainTankY)
        if visible == "t":
            projectile(projectilex,projectiley,life)
        if projectiley >= height - ground_height - projectile_width:
            speed = -10
        elif projectiley <= 0:
            speed = 10
        if projectilex >= width:
            one = -2
        elif projectilex <= 0:
            one = 2
        projectilex += one
        projectiley += speed
        if projectilex - projectile_width < mainTankX + tankWidth and projectilex + projectile_width > mainTankX:
            if projectiley - projectile_width < mainTankY + tankHeight and projectiley + projectile_width > mainTankY:
                over()
        if shooty <= 0:
            shooty = int(mainTankY)
            bullet_state = "ready"
            visibleshoot = True

        if bullet_state == "ready":
            shootx = int(mainTankX)
                    
        if bullet_state == "fire":
            shoot(shootx, shooty)
            shooty -= 20

        if projectilex - projectile_width < shootx + 32 and projectilex + projectile_width > shootx:
            if projectiley - projectile_width < shooty + 32 and projectiley + projectile_width > shooty:
                life -= 20
                bullet_state = "ready"
                shooty = int(mainTankY)
                if life <= 0:
                    win()
                
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()
intro()
