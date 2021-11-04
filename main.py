import pygame
import math
import random
import pygame
from pygame import mixer

# initialise the pygame
pygame.init()

# the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("BackgroundGame.png")
# background sound
mixer.music.load("[Playlist] villain all along.wav")
mixer.music.set_volume(0.09)
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Alien Killer Game ")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('playerAKG.png')
playerX = 360
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

    # Bullet
    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 15
    # Ready means you cant see the bullet on the screen
    bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('Choco Matcha font.otf', 32)

# Coordinate of score
textX = 10
textY = 10
# Game over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 0, 255))
    screen.blit(score, (x, y))


def game_over_txt():
    over_txt = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_txt, (200, 250))


# function for coordinates of player


def player(x, y):
    screen.blit(playerImg, (x, y))


# function for coordinates of enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # Screen Background RGB         R  G  B
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.set_volume(0.05)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerY_change = 0

    # Boundary for player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Boundary and movement for Enemy
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_txt()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.set_volume(0.02)
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(40, 150)

        # Call enemy function
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Call player Function
    player(playerX, playerY)
    show_score(textX, textY)
    # Display Update!
    pygame.display.update()
