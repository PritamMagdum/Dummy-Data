import random   #for generating random
import sys      #for exit the game
import pygame   #for making games in python
from pygame.locals import *   #basic pygame locals
from pygame import *

FPS = 32
SCREENHEIGHT = 511
SCREENWIDTH = 289

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUND = {}
PLAYER = 'Flappy Bird Game/Gallery/sprites/bird.png'
BACKGROUND = 'Flappy Bird Game/Gallery/sprites/background.png'
PIPE = 'Flappy Bird Game/Gallery/sprites/pipe.png'


def welcomeScreen():
    '''Shows the welocome screen before start the game and until shows when the user is not pressed the start button'''
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    
    while True:
        for event in pygame.event.get():
            #if user press the cross or close button
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if user press space or up key then game is start 
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0 ,0 )),
                SCREEN.blit(GAME_SPRITES['player'], (playerx , playery))
                SCREEN.blit(GAME_SPRITES['message'], ( messagex, messagey ))
                SCREEN.blit(GAME_SPRITES['base'], ( basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx =  int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    #create 2 pipes for bliting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my list of upper pipes
    upperPipes = [
            {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
            {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]
    #my list of lower pipes
    lowerPipes = [
            {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
            {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]

    pipeVelX = -4
    
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccVelY = 1

    playerFlapAccv = -8 #velocity while flapping bird
    playerFlapped = False #it is True only when the bird is flapping 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.QUIT()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUND['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) #this function will return true if the player is crashed
        if crashTest:
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score += 1
                print(f"Your score is {score}")
            GAME_SOUND['point'].play()


        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccVelY

        if playerFlapped:
            playerFlapped = False 

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)


        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] +=  pipeVelX
            lowerPipe['x'] += pipeVelX

        # add a new pipe when the first above to the go leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if pipe is out of the screen then remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit out sprites now 
        SCREEN.blit(GAME_SPRITES['background'],(0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
        myDigits = [int(x) for x in list[str(score)]]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    return False


def getRandomPipe():
    '''Generating two pipes (one straight and second rotated)'''
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX =  SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX , 'y' :-y1},
        {'x': pipeX , 'y' : y2}
    ]
    return pipe



if __name__ == "__main__":
    '''This is main point from where our game is start'''
    pygame.init() #initialize all modules of pygame
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Pritam Magdum")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Flappy Bird Game/Gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('Flappy Bird Game/Gallery/sprites/9.png').convert_alpha(),                           
    )

    GAME_SPRITES['message'] = pygame.image.load('Flappy Bird Game/Gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Flappy Bird Game/Gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUND['wing'] = pygame.mixer.Sound('Flappy Bird Game/Gallery/audio/wing.wav')
    GAME_SOUND['die'] = pygame.mixer.Sound('Flappy Bird Game/Gallery/audio/die.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('Flappy Bird Game/Gallery/audio/hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('Flappy Bird Game/Gallery/audio/point.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('Flappy Bird Game/Gallery/audio/swoosh.wav')

    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    while True:
        welcomeScreen() #for shows user until press the start button
        mainGame() #for main game
