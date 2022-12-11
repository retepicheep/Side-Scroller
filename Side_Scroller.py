import pygame
from pygame.locals import *
import os
import sys
import math
import random
from runnerandobjects import *
from levels import *

pygame.init()

W, H = 800, 437
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images','bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
playing = True

clock = pygame.time.Clock()


def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score
               
    return last

def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []
                   
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            run = False
            runner.falling = False
            runner.sliding = False
            runner.jumping = False
            runner.y = 313
        
        if keys[pygame.K_END]:
            run = False
            pygame.quit()

                
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0

        


def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2,0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    runner.draw(win)

    for obstacle in obstacles:
        obstacle.draw(win)

    win.blit(text, (100, 10))
    pygame.display.update()


pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, 3000)
speed = 30

score = 0

run = True
runner = player(200, 313, 64, 64)


obstacles = []
pause = 0
fallSpeed = 0

while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()
        
    score = speed//10 - 3

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            runner.falling = True
            runner.y = 309
            
            if pause == 0:
                pause = 1
                fallSpeed = speed
        if obstacle.x < -64:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.4
    
    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            
        if event.type == USEREVENT+1:
            speed += 1
            
        if event.type == USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
            elif r == 1:
                obstacles.append(spike(810, 0, 48, 310))
                
    if runner.falling == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RSHIFT]:
            if playing == True:
                pygame.mixer.music.stop()
                playing = False
            else:
                pygame.mixer.music.play(-1)
                playing = True
            
        if keys[pygame.K_UP]:
            if not(runner.jumping):
                runner.y = 313
                runner.jumping = True

        if keys[pygame.K_DOWN]:
            if not(runner.sliding):
                runner.sliding = True

    clock.tick(speed)

    redrawWindow()