import pygame
import random
import math

# initialising the pygame

pygame.init()

# creating game window

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('space.jpg')

# Title and logo

pygame.display.set_caption("Space War")
icon = pygame.image.load('catrina.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 350
playerY = 450
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(30, 120))
    enemyX_change.append(20)
    enemyY_change.append(20)

# BULLET
# Ready state(you can't see bullet)
# Fire state(Bullet is moving)

bulletIMG = pygame.image.load('bullet.png')
bulletX = 376
bulletY = 450
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# GAME OVER
over_font = pygame.font.Font('freesansbold.ttf', 128)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (245, 245, 245))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (350, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 40, y + 10))


# Collision

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop

running = True

while running:

    # RGB-->Red,Green,Blue
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -20
            if event.key == pygame.K_RIGHT:
                playerX_change = 20
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # change in position

    playerX += playerX_change

    # Boundary of spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 675:
        playerX = 675

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 350:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200, 200)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # collison

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 450
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()




