import pygame
import sys
import os
import random
import math

pygame.init()
pygame.display.set_caption("Paambu game")
pygame.font.init()
random.seed()

# declare global constant definitions

SPEED = 0.30
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

# check boundaries here we are not limiting boundaries
def checkLimits(snake):
    if(snake.x > SCREEN_WIDTH):
        snake.x = SNAKE_SIZE
    if(snake.x < 0):
        snake.x = SCREEN_WIDTH - SNAKE_SIZE
    if(snake.y > SCREEN_HEIGHT):
        snake.y = SNAKE_SIZE
    if(snake.y < 0):
        snake.y -SCREEN_HEIGHT - SNAKE_SIZE
        
# make class for food ofthe snake let's name it as apple

class Apple:
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("orange") # colour of food
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,APPLE_SIZE,APPLE_SIZE),0)
        
class segment:
    def __init__(self, x, y, direction="UP", color="white"):
        #initial snake will move in up direction
        self.x = x
        self.y = y
        self.direction = direction  # Store the direction name
        self.color = color
    
    
class Snake:
    def __init__(self,x,y):
         self.x = x
         self.y = y
         self.direction = KEY["UP"]
         self.stack = []
         self.stack.append(self)
         blackBox = segment(self.x,self.y + SEPERATION)
         blackBox.direction = KEY["UP"]
         blackBox.color = "NULL"
         self.stack.append(blackBox)
        
    
# Define movment of the snake
    def move(self):
        last_element = len(self.stack)-1
        while(last_element):
            self.stack[last_element].direction = self.stack[last_element].direction
            self.stack[last_element].x = self.stack[last_element -1].x
            self.stack[last_element].y = self.stack[last_element -1].y
            last_element -= 1
        if(len(self.stack) <2):
            last_element = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if(self.stack[0].direction == KEY["UP"]):
            last_segment.y = self.stack[0].y - (SPEED*FPS)
        elif(self.stack[0].direction == KEY["DOWN"]):
            last_segment.y = self.stack[0].y + (SPEED*FPS)
        elif(self.stack[0].direction == KEY["LEFT"]):
            last_segment.x = self.stack[0].x - (SPEED*FPS)
        elif(self.stack[0].direction == KEY["RIGHT"]):
            last_segment.x = self.stack[0].x - (SPEED*FPS)
        self.stack.insert(0,last_segment)
        
    def getHead(self):# It will be always 0 index
        return(self.stack[0]) 
    # now whensnake its food it will grow so for that will add that food to stack
    
    def grow(self):
        last_element = len(self.stack)-1
        self.stack[last_element].direction = self.stack[last_element].direction
        if(self.stack[last_element].direction == KEY["up"]):
            newSegment = segment(self.stack[last_element].x,self.stack[last_element].y - SNAKE_SIZE)
            blackBox = segment(newSegment.x, newSegment.y - SEPERATION)
            
        elif(self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = segment(self.stack[last_element].x,self.stack[last_element].y + SNAKE_SIZE)
            blackBox = segment(newSegment.x, newSegment.y + SEPERATION)
            
        elif(self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = segment(self.stack[last_element].x - SNAKE_SIZE, self.stack[last_element].y)
            blackBox = segment(newSegment.x - SEPERATION , newSegment.y)  
            
        elif(self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = segment(self.stack[last_element].x - SNAKE_SIZE, self.stack[last_element].y)
            blackBox = segment(newSegment.x - SEPERATION , newSegment.y)  

        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)
        
    def iterateSegments(self,delta):
        pass
    
    def setDirection(self,direction):
        if(self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY["left"] and direction == KEY["RIGHT"]):
            pass
        elif(self.direction == KEY["UP"] and direction == KEY["DOWN"] or self.direction == KEY["UP"] and direction == KEY["DOWN"]):
            pass
        else:
            self.direction = direction
    
    def get_rect(self):
        rect = (self.x,self.y)
        return rect
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    #Define function of crashing when snake eatitself
    def checkCrashing(self):
        counter = 1
        while (counter < len(self.stack)-1):
            if(checkCollision(self.stack[0],SNAKE_SIZE , self.stack[counter],SNAKE_SIZE) and self.stack[counter].color != "NULL"):
                return True
            counter += 1
        return False
    
    def draw(self,screen):
        pygame.draw.rect(screen,pygame.Color.Color("green"), (self.stack[0].x , self.stack[0].y,SNAKE_SIZE,SNAKE_SIZE),0)
        
        counter = 1
        while(counter <len(self.stack)):
            if(self.stack[counter].color == "NULL"):
                counter += 1
                continue
            
            pygame.draw.rect(screen, pygame.color.Color("yellow"), (self.stack[counter].x,self.stack[counter].y, SNAKE_SIZE , SNAKE_SIZE),0)
            counter += 1
        
        
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
        
        if event.type == pygame.QUIT:
            sys.exit(0)
    return None
            
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
    
    #initialization of snake
    mySnake = Snake(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    mySnake.setDirection["UP"]
    mySnake.move()
    start_segment = 3 #initial segment of snake
    while(start_segment > 0):
        mySnake.grow()
        mySnake.move()
        start_segment -= 1
