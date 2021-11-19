from random import randint
from math import sqrt, pow
from pygame import mixer
import pygame

# Icon
icon = pygame.image.load('img\\ufo.png')
pygame.display.set_icon(icon)

# Screen, Intializing and Title
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Player
playerIcon = pygame.image.load('img\\space.png')
playerX = 370
playerY = 450
playerX_change = 0

# Bullet
bulletIcon = pygame.image.load('img\\bullet.png')
bulletY = 450
bulletX = 0
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_v = 0
f = pygame.font.Font('font\\Roboto-Black.ttf', 30)

textX = 10
textY = 10


def showScore(x, y):
    score = f.render("Score: "+str(score_v), True, (255, 255, 255))
    screen.blit(score, (x, y))


def spwanEnemy():
    global enemyIcon, enemyY, enemyX, enemyX_change, enemyY_change, numberEnimies

    enemyIcon = []
    enemyY = []
    enemyX = []
    enemyX_change = []
    enemyY_change = []
    numberEnimies = 3

    for i in range(numberEnimies):
        enemyIcon.append(pygame.image.load('img\\alien.png'))
        enemyY.append(randint(50, 200))
        enemyX.append(randint(100, 300))
        enemyX_change.append(2)
        enemyY_change.append(40)

    # Ready - Can't see bullet
    # Fire - Can see bullet


# Enemy
spwanEnemy()


def drawPlayer(x, y):
    screen.blit(playerIcon, (x, y))


def drawEnemy(x, y, i):
    screen.blit(enemyIcon[i], (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIcon, (x+16, y+10))


def isColistion(eX, eY, bX, bY):
    return True if sqrt(pow(eX-eY, 2)+pow(bX-bY, 2)) < 50 else False

def gameOverText():
    o  = pygame.font.Font('font\\Roboto-Black.ttf',80)
    over = o.render("Game Over", True, (255, 0, 0))
    screen.blit(over, (200,250))

# Game Loop
executing = True

mixer.music.load('music\\background.wav')
mixer.music.play(-1)

while executing:
    # Background
    bg = pygame.image.load("img\\bg.jpg")
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            elif event.key == pygame.K_RIGHT:
                playerX_change = 4
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bullet_state == "ready":
                    b = mixer.Sound('music\\laser.wav')
                    b.play()
                    bulletY_change = 8 
                    bulletX = playerX
                    fireBullet(playerX, bulletY)


            elif event.key == pygame.K_p:
                score_v = score_v + 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX < 0:
        playerX = 0

    if playerX >= 736:
        playerX = 736

    for i in range(numberEnimies):
        if enemyY[i] > 430:
            for j in range(numberEnimies):
                enemyY[j] = 2000
            gameOverText()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        if enemyX[i] < 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        col = isColistion(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            c = mixer.Sound('music\\explosion.wav')
            c.play()
            bulletY = 450
            bullet_state = "ready"
            score_v += 1
            spwanEnemy()

        drawEnemy(enemyX[i], enemyY[i], i)

    if bulletY < 0:
        bullet_state = "ready"
        bulletY = 450

    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    drawPlayer(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
