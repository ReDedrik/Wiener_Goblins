import pygame
import random
import math
import sys

# importing pygame and initializing it allows us to access all the features
pygame.init()

# using the screen from pygame and using pixels of 800 wide and 600 tall
screen = pygame.display.set_mode((1710, 1000))

background = pygame.image.load('pixelstars.jpg')

# Title changing command
pygame.display.set_caption("Wiener Goblins")

# Icon changing command
icon = pygame.image.load('hot-dog.png')
pygame.display.set_icon(icon)

# Score
score = 0

textX = 10
textY = 10

# Player icon and coordinates
playerImg = pygame.image.load('space-invaders.png')
playerX = 780
playerY = 880
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10


# Enemy icon and coords
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('hot-dog.png'))
    enemyX.append(random.randint(50, 1500))
    enemyY.append(random.randint(50, 300))
    enemyX_change.append(1)
    enemyY_change.append(75)

# Text Color
white = (255,255,255)


# Player Bullet
playerbulletImg = pygame.image.load('ketchup.png')
playerbulletX = 0
playerbulletY = 880
playerbulletY_change = 1.5
playerbullet_state = "ready"

# CLASSES

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.lasers_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y), 0)










# player position (blit = draw)
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global playerbullet_state
    playerbullet_state = "fire"
    screen.blit(playerbulletImg, (x + 16, y - 20))


def isCollision(enemyX, enemyY, playerbulletX, playerbulletY):
    distance = math.sqrt((math.pow(enemyX - playerbulletX, 2)) + (math.pow(enemyY - playerbulletY, 2)))
    if distance < 50:
        return True
    else:
        return False


# Game Over
gameoverfont = pygame.font.Font('NEONLEDLight.ttf', 1000)


def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, white)
    screen.blit(score_value, (x, y))


def gameover():
    over_text = font.render("GAME OVER", True, white)
    screen.blit(over_text, (650, 460))


# infinite loop that sets the window to running,
# when the "X" button is clicked then it sets 'running' to false,
# which terminates the loop and closes the window.

running = True
FPS = 60
level = 1
lives = 5
font = pygame.font.Font('NEONLEDLight.ttf', 61)
while running:
    # RGB colors
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if playerbullet_state is "ready":
                    fire_bullet(playerX, playerbulletY)
                    playerbulletX = playerX
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    # Player movement and boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1536:
        playerX = 1536

    # Calling player and enemies to appear
    player(playerX, playerY)

    # Enemy movement and bounce off boundaries

    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 720:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameover()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]
            if enemyY[i] >= 500:
                enemyX_change[i] = 0.4
        elif enemyX[i] >= 1536:
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], playerbulletX, playerbulletY)
        if collision:
            playerbulletY = 880
            playerbullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(600, 1000)
            enemyY[i] = random.randint(50, 200)
        enemy(enemyX[i], enemyY[i], i)

    # Player bullet movement
    if playerbulletY <= 0:
        playerbulletY = 880
        playerbullet_state = "ready"

    if playerbullet_state is "fire":
        fire_bullet(playerbulletX, playerbulletY)
        playerbulletY -= playerbulletY_change

    show_score(textX, textY)

    # updating to fill screen color and show other images
    pygame.display.update()
