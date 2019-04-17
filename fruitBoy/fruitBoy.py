#imports
import pygame
import random

#general values
red = (123,59,62)
blue = (0,0,205)
green = (62,123,59)
black = (0,0,0)

#game values
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
myfont = pygame.font.SysFont('jokerman', 20)
screenw = 600
screenh = 800
screen = [screenw,screenh]
win = pygame.display.set_mode(screen)

#music/effects
pygame.mixer.music.load('gamemusic.mp3')
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play(-1)
bomb = pygame.mixer.Sound('bomb.wav')
jump = pygame.mixer.Sound('jump.wav')
teleport = pygame.mixer.Sound('teleport.wav')
jump.set_volume(.25)


#boy class
class Boy:
    def __init__(self):
        self.h = 80
        self.w = 40
        self.x = 300
        self.y = 700
        self.yspeed = 0
        self.xspeed = 12
        self.xspeedh = 12
        self.gravity = 1
        self.accel = .3
        self.jumpval = 10
        self.jc = 0
        self.maxjumps = 3
        self.notmove = True
        self.jmarker = False
        self.movelb = False
        self.moverb = False
    def movel(self):
        self.notmove = False
        if self.moverb == True:
            self.xspeed = self.xspeedh
        self.x -= self.xspeed
        self.xspeed += self.accel
        self.movelb = True
        self.moverb = False
    def mover(self):
        self.notmove = False
        if self.movelb == True:
            self.xspeed = self.xspeedh
        self.x += self.xspeed
        self.xspeed += self.accel
        self.moverb = True
        self.movelb = False
    def jump(self):
        if self.jc < self.maxjumps:
            jump.play()
            self.yspeed -= self.jumpval
            self.y += self.yspeed
            self.jmarker = True
            self.jc += 1
    def fall(self):
        if self.y < floor - npc.h or self.jmarker == True:
            self.y += self.yspeed
            self.yspeed += self.gravity
            self.jmarker = False
        else:
            self.y = floor - npc.h
            self.yspeed = 0
            self.jc = 0
    def reset(self):
        self.x = 300
        self.y = 700
        self.yspeed = 0
        self.xspeed = 12
        self.notmove = True
        self.jmarker = False
        self.movelb = False
        self.moverb = False

#fruit class             
class Fruit():
    def __init__(self):
        self.randomizer = random.randint(0,50)
        self.x =random.randint(10,screenw-10)
        self.y =random.randint(-800,0)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.speed = 0
        self.gravity = 1
        self.implode = False
        self.size = random.randint(10,20)
    def fall(self):
        self.y += self.speed
        if self.speed < 15:
            self.speed += self.gravity

#update/draw
def update():
    #text updates
    win.blit(bg,(0,0))
    if reset == False:
        win.blit(scorez,(250,0))
        win.blit(timez,(250,25))
        if maxfruitfall == True:
            win.blit(fruitfallbuffz,(210,300))
    if reset == True:
        if start == True:
            win.blit(welcome,(120,300))
        else:
            win.blit(scorez2,(250,100))
            win.blit(hsz,(250,125))
    #npc update
    if npc.y < floor -npc.h - 1:
        win.blit(boyj,(npc.x,npc.y))
    elif npc.notmove == True:
        win.blit(boy,(npc.x,npc.y))
    elif npc.moverb == True:
        win.blit(boyr,(npc.x,npc.y))
    elif npc.movelb == True:
        win.blit(boyl,(npc.x,npc.y))    
    #fruit update
    for fruit in fruits:
        if fruit.implode == True:
            win.blit(explosionz,(implodex,implodey))
        if fruit.randomizer < maxfruitbuffprob:
            win.blit(powerup,(fruit.x,fruit.y))
        else:
            pygame.draw.circle(win,fruit.color,[fruit.x,fruit.y],fruit.size)
    pygame.display.flip()

#populize list of fruits
def fruitpopulize(fruits):
    while len(fruits) < maxfruits:
        fruit = Fruit()
        fruits.append(fruit)

#object initialization
remaxfruits=4
maxfruits = 4
maxfruitbuff = 30
maxfruitbuffprob = 1
retime = 61
time = 61
score = 0
scoreincrease = 1
hs = 0
timedelay = 30
timechange = .04
floor = 780
teleportdist = 100
explosion = False
reset = True
start = True
maxfruitfall = False
#load all sprites
powerup = pygame.image.load('powerup.png')
bg = pygame.image.load('backd2.png')
boy = pygame.image.load('boy.png')
boyj = pygame.image.load('boyj.png')
boyr = pygame.image.load('boyr.png')
boyl = pygame.image.load('boyl.png')
explosionz = pygame.image.load('explosion.png')
#initialize npc
npc = Boy()
#initialize fruit list
fruits = []
fruitpopulize(fruits)

#game loop
run = True
while run:
    pygame.time.delay(timedelay)
    npc.fall()
    time -= timechange
        
    #fruits
    for idx in range(maxfruits):
        if npc.x < fruits[idx].x < npc.x+npc.w and  npc.y+npc.h > fruits[idx].y > npc.y:
            #maxfruit buff
            if fruits[idx].randomizer < maxfruitbuffprob:
                maxfruitfall = True
                maxfruits = maxfruitbuff
                fruitpopulize(fruits)
                maxftime = int(time)
            #fruit implosion coord
            implodex = npc.x
            implodey = npc.y
            #score per fruit
            score += scoreincrease
            #delete captured fruit
            del fruits[idx]
            #create new fruit
            fruit = Fruit()
            fruits.append(fruit)
            fruits[idx].implode = True
            #play fruit capture sound
            bomb.play()
        #delete floor fruits
        if fruits[idx].y > floor - fruits[idx].size:
            del fruits[idx]
            fruit = Fruit()
            fruits.append(fruit)
        #fruit fall
        fruits[idx].fall()
    #maxfruit buff reset
    if maxfruitfall == True:
        if int(maxftime) - int(time) > 10:
            fruits = []
            maxfruits = remaxfruits
            fruitpopulize(fruits)
            maxfruitfall = False

    #high score tracker
    if score > hs:
        hs = score

    #font rendering
    scorez = myfont.render('Score: ' + str(score),1,green)
    timez = myfont.render('Time: ' + str(int(time)),1,green)
    welcome = myfont.render('Welcome To FruitBoy Press P To Begin',1,green)
    scorez2 = myfont.render('Last Score: '+str(score),1,green)
    hsz = myfont.render('High Score: '+str(hs),1,green)
    fruitfallbuffz = myfont.render('MAX FRUIT FALL!',1,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    #event handler
    npc.notmove = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        npc.mover()
    if keys[pygame.K_LEFT]:
        npc.movel()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
                exit()
            if event.key == pygame.K_SPACE:
                npc.jump()
            if event.key == pygame.K_DOWN:
                if npc.notmove == False:
                    if npc.moverb == True:
                        teleport.play()
                        npc.x += teleportdist
                    if npc.movelb == True:
                        teleport.play()
                        npc.x -= teleportdist
    #boundries
    if npc.x > screenw - npc.w:
        npc.x = screenw - npc.w
    if npc.x < 0:
        npc.x = 0

    #reset mechanic
    if int(time) == 0:
        reset = True
    if reset == True:
        fruits = []
        score = 0
        npc.reset()
        while reset:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        reset = False
                        time = retime
                        fruitpopulize(fruits)
                        if start == True:
                            start = False
            update()
            
    #game update                
    update()
    

