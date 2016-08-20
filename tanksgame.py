import pygame
import time
import random
#import cx_Freeze


pygame.init()
display_width=800
display_height=600

#fire_sound=pygame.mixer.Sound("boom.wav")
#explosion_sound=pygame.mixer.Sound("explosion.wav")

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Tanks')

white=(255,255,255)
black=(0,0,0) 
green=(34,177,76)
yellow=(200,200,0)
lightyellow=(255,255,0)
red=(200,0,0)
lightred=(255,0,0)
lightgreen=(0,255,0)
clock=pygame.time.Clock()

tankwidth=40
tankheight=20
turretwidth=5
wheelwidth=5
groundheight=35

verysmallfont=pygame.font.SysFont("comsansms",22)
smallfont=pygame.font.SysFont("comicsansms",25)
medfont=pygame.font.SysFont("comicsansms",50)
largefont=pygame.font.SysFont("comicsansms",75)



def score(score):

    text=smallfont.render("Score:"+str(score),True,black)
    gameDisplay.blit(text,[0,0])

def text_to_button(msg,color,buttonx,buttony,buttonwidth,buttonheight,size="small"):
    textSurf,textRect=text_objects(msg,color)
    textRect.center=(buttonx+(buttonwidth/2),buttony+(buttonheight/2))
    gameDisplay.blit(textSurf,textRect)

def tank(x,y,turPos):
    x=int(x)
    y=int(y)

    possibleTurrets=[(x-27,y-2),
                     (x-26,y-5),
                     (x-25,y-8),
                     (x-23,y-12),
                     (x-20,y-14),
                     (x-18,y-15),
                     (x-15,y-17),
                     (x-13,y-19),
                     (x-11,y-21)]

    pygame.draw.circle(gameDisplay,black,(x,y),int(tankheight/2))
    pygame.draw.rect(gameDisplay,black,(x-tankheight,y,tankwidth,tankheight))
    pygame.draw.line(gameDisplay,black,(x,y),possibleTurrets[turPos],turretwidth)
    z=x-15
    while z<x+20:
         pygame.draw.circle(gameDisplay,black,(z,y+20),wheelwidth)
         z+=5
    return possibleTurrets[turPos]

def enemy_tank(x,y,turPos):
    x=int(x)
    y=int(y)

    possibleTurrets=[(x+27,y-2),
                     (x+26,y-5),
                     (x+25,y-8),
                     (x+23,y-12),
                     (x+20,y-14),
                     (x+18,y-15),
                     (x+15,y-17),
                     (x+13,y-19),
                     (x+11,y-21)]

    pygame.draw.circle(gameDisplay,black,(x,y),int(tankheight/2))
    pygame.draw.rect(gameDisplay,black,(x-tankheight,y,tankwidth,tankheight))
    pygame.draw.line(gameDisplay,black,(x,y),possibleTurrets[turPos],turretwidth)
    z=x-15
    while z<x+20:
         pygame.draw.circle(gameDisplay,black,(z,y+20),wheelwidth)
         z+=5
    return possibleTurrets[turPos]



def game_controls():
    gcont=True

    while gcont:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        message_to_screen("Controls",green,-100,size="large")
        message_to_screen("Fire:Spacebar",black,-30)
        message_to_screen("Move Turret: Up and Down arrows",black,10)
        message_to_screen("Move Tank: Left and Right Arrows",black,50)
        message_to_screen("Power Increase: D",black,90)
        message_to_screen("Power Decrease: A",black,130)
        message_to_screen("Pause: P",black,170)
        button("Play",150,500,100,50,green,lightgreen,action="play")
        #button("Controls",350,500,100,50,yellow,lightyellow,action="controls")
        button("Quit",550,500,100,50,red,lightred,action="quit")
        pygame.display.update()

        clock.tick(15)



def button(text,x,y,width,height,inactive,active,action=None):
    cur=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x<cur[0]<x+width and y<cur[1]<y+height:
       pygame.draw.rect(gameDisplay,active,(x,y,width,height))
       if click[0]==1 and action!=None:
           if action=="play":
               gameLoop()
           elif action=="controls":
               game_controls()
           elif action=="quit":
               quit()
    else:
        pygame.draw.rect(gameDisplay,inactive,(x,y,width,height))

    text_to_button(text,black,x,y,width,height)


def text_objects(text,color,size="small"):
    if size=="verysmall":
        textSurface=verysmallfont.render(text,True,color)
    if size=="small":
        textSurface=smallfont.render(text,True,color)
    if size=="medium":
        textSurface=medfont.render(text,True,color)
    if size=="large":
        textSurface=largefont.render(text,True,color)
    return textSurface,textSurface.get_rect()


def message_to_screen(msg,color,y_displace=0,size="small"):
    textSurf,textRect=text_objects(msg,color,size)
    textRect.center=(display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)


def pause():
    gamePause=True
    message_to_screen(" Paused",
                          red,
                         -100,
                          "large")
    message_to_screen("Press C to continue or Q to Quit",
                          black,
                          20,
                          "small")
    pygame.display.update()

    while gamePause:
        for event in pygame.event.get():
            if event==pygame.QUIT:
                pygame.quit()
                quit();
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit();
                elif event.key==pygame.K_c:
                    gamePause=False


        clock.tick(5)

def barrier(xloc,randomheight,barrier_width):
    pygame.draw.rect(gameDisplay,black,[xloc,display_height-randomheight,barrier_width,randomheight])

def explosion(x,y,size=50):
     explode=True

     while explode:
         for event in pygame.event.get():
             if event.type==pygame.QUIT:
                 pygame.quit()
                 quit()

         startingpoint=x,y

         colorchoices=[red,lightred,yellow,lightyellow]

         magnitude=1;
         while magnitude < size:
             exploding_bit_x=x+random.randrange(-1*magnitude,magnitude)
             exploding_bit_y=y+random.randrange(-1*magnitude,magnitude)
             pygame.draw.circle(gameDisplay,colorchoices[random.randrange(0,4)],(exploding_bit_x,exploding_bit_y),random.randrange(1,5))
             magnitude+=1

             pygame.display.update()

             clock.tick(120)

         explode=False


def health_bars(player_health,enemy_health):
    if player_health>75:
        player_health_color=green
    elif player_health>50:
        player_health_color=yellow
    else:
        player_health_color=red
    if enemy_health>75:
        enemy_health_color=green
    elif enemy_health>50:
        enemy_health_color=yellow
    else:
        enemy_health_color=red

    textSurf,textRect=text_objects("Health:"+str(player_health),black,"verysmall")
    textRect.center=715,10
    gameDisplay.blit(textSurf,textRect)
    textSurf,textRect=text_objects("Health:"+str(enemy_health),black,"verysmall")
    textRect.center=55,10
    gameDisplay.blit(textSurf,textRect)

    pygame.draw.rect(gameDisplay,player_health_color,(680,25,player_health,25))
    pygame.draw.rect(gameDisplay,enemy_health_color,(20,25,enemy_health,25))

def fireshell(xy,tankx,tanky,turpos,gunpower,xloc,barrier_width,randomheight,enemytankx,enemytanky):
    #pygame.mixer.Sound.play(fire_sound)
    fire=True
    damage=0
    startingshell=list(xy)
    print("FIRE!!")

    while fire:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        print(startingshell[0],startingshell[1])
        pygame.draw.circle(gameDisplay,red,(startingshell[0],startingshell[1]),5)

        startingshell[0]-=(12-turpos)*2

        startingshell[1]+=int((((startingshell[0]-xy[0])*0.015/(gunpower/50))**2)-(turpos+turpos/(12-turpos)))

        if startingshell[1]>display_height-groundheight:
            print("Last shell:",startingshell[0],startingshell[1])
            hit_x=int((startingshell[0]*(display_height-groundheight))/startingshell[1])
            hit_y=int(display_height-groundheight)
            print("Impact:",hit_x,hit_y)

            if enemytankx+10>hit_x>enemytankx-10:
                print("Critical Hit!")
                damage=20
            elif enemytankx+15>hit_x>enemytankx-15:
                print("Hard Hit!")
                damage=15
            elif enemytankx+25>hit_x>enemytankx-25:
                print("Medium Hit!")
                damage=10
            elif enemytankx+35>hit_x>enemytankx-35:
                print("Light Hit!")
                damage=5


            explosion(hit_x,hit_y)
            fire=False

        check_x_1=startingshell[0]<=xloc+barrier_width
        check_x_2=startingshell[0]>=xloc

        check_y_1=startingshell[1]<=display_height
        check_y_2=startingshell[1]>=display_height-randomheight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
           # print("Last shell:",startingshell[0],startingshell[1])
            hit_x=int((startingshell[0]))
            hit_y=int(startingshell[1])
            #print("Impact:",hit_x,hit_y)
            explosion(hit_x,hit_y)
            fire=False


        pygame.display.update()

        clock.tick(100)

    return damage

def e_fireshell(xy,tankx,tany,turpos,gunpower,xloc,barrier_width,randomheight,ptankx,ptanky):
    #pygame.mixer.Sound.play(fire_sound)
    currentpower=1;
    power_found=False
    damage=0

    while not power_found:
        currentpower+=1
        if currentpower>100:
         power_found=True
        fire=True

        startingshell=list(xy)
        while fire:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()

            #print(startingshell[0],startingshell[1])
           #  pygame.draw.circle(gameDisplay,red,(startingshell[0],startingshell[1]),5)

            startingshell[0]+=(12-turpos)*2

            startingshell[1]+=int((((startingshell[0]-xy[0])*0.015/(currentpower/50))**2)-(turpos+turpos/(12-turpos)))

            if startingshell[1]>display_height-groundheight:
                hit_x=int((startingshell[0]*(display_height-groundheight))/startingshell[1])
                hit_y=int(display_height-groundheight)
               # explosion(hit_x,hit_y)
                if ptankx+15>hit_x>ptankx-15:
                    #print("Target Acquired!!")
                    power_found=True
                fire=False

            check_x_1=startingshell[0]<=xloc+barrier_width
            check_x_2=startingshell[0]>=xloc

            check_y_1=startingshell[1]<=display_height
            check_y_2=startingshell[1]>=display_height-randomheight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x=int((startingshell[0]))
                hit_y=int(startingshell[1])
                #explosion(hit_x,hit_y)
                fire=False

    fire=True

    startingshell=list(xy)
   # print("FIRE!!")

    while fire:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        #print(startingshell[0],startingshell[1])
        pygame.draw.circle(gameDisplay,red,(startingshell[0],startingshell[1]),5)

        startingshell[0]+=(12-turpos)*2
        rand_power=random.randrange(int(currentpower*0.9),int(currentpower*1.1))
        startingshell[1]+=int((((startingshell[0]-xy[0])*0.015/(rand_power/50))**2)-(turpos+turpos/(12-turpos)))

        if startingshell[1]>display_height-groundheight:
            #print("Last shell:",startingshell[0],startingshell[1])
            hit_x=int((startingshell[0]*(display_height-groundheight))/startingshell[1])
            hit_y=int(display_height-groundheight)
            #print("Impact:",hit_x,hit_y)

            if ptankx+10>hit_x>ptankx-10:
                #print("Critical Hit!")
                damage=20
            elif ptankx+15>hit_x>ptankx-15:
                #print("Hard Hit!")
                damage=15
            elif ptankx+25>hit_x>ptankx-25:
                #print("Medium Hit!")
                damage=10
            elif ptankx+35>hit_x>ptankx-35:
                #print("Light Hit!")
                damage=5


            explosion(hit_x,hit_y)
            fire=False

        check_x_1=startingshell[0]<=xloc+barrier_width
        check_x_2=startingshell[0]>=xloc

        check_y_1=startingshell[1]<=display_height
        check_y_2=startingshell[1]>=display_height-randomheight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            #print("Last shell:",startingshell[0],startingshell[1])
            hit_x=int((startingshell[0]))
            hit_y=int(startingshell[1])
            #print("Impact:",hit_x,hit_y)
            explosion(hit_x,hit_y)
            fire=False

        pygame.display.update()
        clock.tick(100)
    return damage


def power(level):
    text=smallfont.render("Power:"+str(level)+"%",True,black)
    gameDisplay.blit(text,[display_width/2-20,0])


def game_intro():
    intro=True

    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()


            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                elif event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)

        message_to_screen("Welcome to Tanks",green,-100,size="large")
        message_to_screen("The objective is to shoot and destroy",black,-30)
        message_to_screen("the enemy tank before they destroy you!!",black,10)
        message_to_screen("The more enemies you destroy, the harder they get.",black,50)

        button("Play",150,500,100,50,green,lightgreen,action="play")
        button("Controls",350,500,100,50,yellow,lightyellow,action="controls")
        button("Quit",550,500,100,50,red,lightred,action="quit")
        pygame.display.update()

        clock.tick(15)

def game_over():
    gameover=True

    while gameover:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        message_to_screen("Game Over",green,-100,size="large")
        message_to_screen("You died.",red,-30)

        button("Play Again",150,500,150,50,green,lightgreen,action="play")
        #button("Controls",350,500,100,50,yellow,lightyellow,action="controls")
        button("Quit",550,500,100,50,red,lightred,action="quit")
        pygame.display.update()

        clock.tick(15)


def you_win():
    youwin=True

    while youwin:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()


        gameDisplay.fill(white)
        message_to_screen("You Win!!",green,-100,size="large")
        message_to_screen("Congratulations",black,-30)

        button("Play Again",150,500,150,50,green,lightgreen,action="play")
        #button("Controls",350,500,100,50,yellow,lightyellow,action="controls")
        button("Quit",550,500,100,50,red,lightred,action="quit")
        pygame.display.update()

        clock.tick(15)



def gameLoop():
    gameOver=False
    gameExit=False
    FPS=15

    player_health=100
    enemy_health=100

    maintankx=display_width*0.9
    maintanky=display_height*0.9
    tankmove=0
    currturpos=0
    changetur=0

    enemytankx=display_width*0.1
    enemytanky=display_height*0.9

    barrier_width=50

    xloc=(display_width/2)+random.randint(-0.1*display_width,0.1*display_width)
    randomheight=random.randrange(0.2*display_height,0.55*display_height)

    fire_power=50
    power_change=0

    while not gameExit:
        if gameOver==True:
            #gameDisplay.fill(white)
            message_to_screen("Game Over!!",
                              red,
                              -50,
                              size="large")
            message_to_screen("Press C to play again or Q to Quit.",
                              black,
                              50,
                              size="medium")
            pygame.display.update()

            while gameOver==True:

                for event in pygame.event.get():
                     if event.type==pygame.QUIT:
                         gameExit=True
                         gameOver=False

                     if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_q:
                            gameExit=True
                            gameOver=False

                        elif event.key==pygame.K_c:
                         gameLoop()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    tankmove=-5
                elif event.key==pygame.K_RIGHT:
                    tankmove=5
                elif event.key==pygame.K_UP:
                   changetur=1
                elif event.key==pygame.K_DOWN:
                   changetur=-1
                elif event.key==pygame.K_p:
                    pause()
                elif event.key==pygame.K_SPACE:
                    enemy_damage=fireshell(gun,maintankx,maintanky,currturpos,fire_power,xloc,barrier_width,randomheight,enemytankx,enemytanky)
                    enemy_health-=enemy_damage

                    possibleMovement=['f','r']
                    moveidx=random.randrange(0,2)

                    for x in range(random.randrange(0,10)):

                        if (display_width)*0.4>enemytankx>display_width*0.03:
                            if possibleMovement[moveidx]=="f":
                                enemytankx+=5
                            elif possibleMovement[moveidx]=="r":
                                enemytankx-=5
                                gameDisplay.fill(white)
                                health_bars(player_health,enemy_health)
                                gun=tank(maintankx,maintanky,currturpos)
                                enemy_gun=enemy_tank(enemytankx,enemytanky,8)

                                fire_power+=power_change
                                power(fire_power)

                                barrier(xloc,randomheight,barrier_width)
                                gameDisplay.fill(green,rect=[0,display_height-groundheight,display_width,groundheight])
                                pygame.display.update()
                                clock.tick(FPS)

                    damage=e_fireshell(enemy_gun,enemytankx,enemytanky,8,50,xloc,barrier_width,randomheight,maintankx,maintanky)
                    player_health-=damage


                elif event.key==pygame.K_a:
                    power_change-=1
                elif event.key==pygame.K_d:
                    power_change+=1


            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    tankmove=0
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    changetur=0
                if event.key==pygame.K_a or event.key==pygame.K_d:
                    power_change=0


        maintankx+=tankmove
        currturpos+=changetur

        if currturpos>8:
            currturpos=8
        elif currturpos<0:
            currturpos=0

        if maintankx-(tankwidth/2)<xloc+barrier_width:
            maintankx+=5

        gameDisplay.fill(white)
        health_bars(player_health,enemy_health)
        gun=tank(maintankx,maintanky,currturpos)
        enemy_gun=enemy_tank(enemytankx,enemytanky,8)

        fire_power+=power_change
        if fire_power>100:
            fire_power=100
        elif fire_power<1:
            fire_power=1

        power(fire_power)

        barrier(xloc,randomheight,barrier_width)
        gameDisplay.fill(green,rect=[0,display_height-groundheight,display_width,groundheight])
        pygame.display.update()

        if player_health<1:
            game_over()
        elif enemy_health<1:
            you_win()

        clock.tick(FPS)


    pygame.quit()
    quit()


game_intro()
gameLoop()