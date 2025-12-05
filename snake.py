import pygame
import sys
import os
import random
import math

pygame.init()
pygame.display.setCaption("Paambu game")
pygame.font.init()
random.speed()

# declare global constant definitions

speed = 0.30
SNAKE_SIZE = 9
APPLE_SIZE = SNAKE_SIZE
SEPERATION = 10 #seperation between two pixel
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
FPS = 25
KEY = {"UP":1,"DOWN":2,"LEFT":3,"RIGHT":4}

#initialize screen
screen = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_HEIGHT),pygame.HWSURFACE)


score_font = pygame.font.Font(None,38)
score_numb_font = pygame.font.Font(None,28)
game_over_font = pygame.font.Font(None,48)
play_again_font = pygame.font.Font(None,28)
score_msg = score_font.render("Score : ",1,pygame.Color("green"))
score_msg_size = score_font.size("Score")
background_color = pygame.Color(0,0,0)
black = pygame.Color(0,0,0)


# for clock at the left corner
gameClock = pygame.time.Clock()

def checkCollision(posA,As,posB,Bs):
    if(posA.x < posB.x+Bs and posA.x+As > posB.x and posA.y < posB.y+Bs and posA.y+As > posB.y):
        return True
    return False
    
    

#define key
def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            
            elif event.key == pygame.K_ESCAPE:#for exit
                return "exit"
            elif event.key == pygame.K_y:#for continue
                return "yes"
            elif event.key == pygame.K_n:#for continue
                return "no"
        
        if event.type == pygame.QUITE:
            sys.exit(0)
            
def endGame():
    message = game_over_font.render("Soli mudinchu",1,pygame.Color("white"))
    message_play_again = play_again_font.render("Thirumba vaariyaa ? (Y/N)",1,pygame.Color("green"))
    screen.blit(message,(320,240))
    screen.blit(message_play_again,(320+12,240+40))
    
    pygame.display.flip()
    pygame.display.update()
    
    mkey = getKey()
    while(mkey != "exit"):
        if(mkey == "yes"):
            main()
        elif(mkey == "no"):
            break
        mkey = getKey()
        gameClock.tick(FPS)
    sys.exit(0)
    
def drawScore(score):
    score_numb = score_numb_font.render(str(score),1,pygame.Color("red"))
    screen.blit(score_msg,(SCREEN_WIDTH - score_msg_size[0]-60,10))
    screen.blit(score_numb,(SCREEN_WIDTH - 45,14))
    
    
def drawGameTime(gameTime):
    game_time = score_font.render("Time:" , 1,pygame.Color("white"))
    game_time_numb = score_numb_font.render(str(gameTime/1000),1,pygame.Color("white"))
    screen.blit(game_time,(30,10))
    screen.blit(game_time_numb,(105,14))
    
def exitScreen():
    pass

    
def main():
    score = 0
