import pygame
import random
import math
import sys

# importing pygame and initializing it allows us to access all the features
pygame.init()

# using the screen from pygame and using pixels of 800 wide and 600 tall
screen_width = 1600
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

background = pygame.image.load('pixelstars.jpg')

# Title changing command
pygame.display.set_caption("Wiener Goblins")

running = True

# Icon changing command
icon = pygame.image.load('hot-dog.png')
pygame.display.set_icon(icon)

# Score
score = 0
font = pygame.font.Font('NEONLEDLight.ttf', 56)
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
num_of_enemies = 7

# Enemy icon and coords
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('hot-dog.png'))
    enemyX.append(random.randint(50, 1500))
    enemyY.append(random.randint(50, 300))
    enemyX_change.append(1)
    enemyY_change.append(75)

# Text Color
white = (255, 255, 255)
gray = (102, 102, 102)

# Start menu strings
howdy = "howdy do buccaroo"
sup = "how's it going?"

# Bullet
playerbulletImg = pygame.image.load('ketchup.png')
playerbulletX = 0
playerbulletY = 880
playerbulletY_change = 1.5
playerbullet_state = "ready"


# Start button creation
def create_button(msg, x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    # mouse position is stored in 'mouse' variable
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            first_level()
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))
    # start button text
    startbuttontext = font.render(msg, True, white)
    screen.blit(startbuttontext, (int(890 + (width / 2)), int(y + (y / 2))))

# Start Menu
def start_menu(howdy, sup):
    global running, playerbullet_state, playerX, playerbulletY, playerX_change, playerbulletX
    startText = font.render("Wiener Goblins", True, gray)
    howdyText = font.render(howdy, True,gray)
    supText = font.render(sup, True, gray)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(howdyText, (5, 0))
        screen.blit(supText, (1580, 0))
        screen.blit(startText,((screen_width - startText.get_width()) / 2, 0))

        create_button("START", 650, 460, 300, 60, gray, white)

        while running:
            # RGB colors
            screen.fill((51, 0, 0))
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


# Clock
clock = pygame.time.Clock()

# Score


# Game Over
gameoverfont = pygame.font.Font('NEONLEDLight.ttf', 1000)


def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def gameover():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (650, 460))


# infinite loop that sets the window to running,
# when the "X" button is clicked then it sets 'running' to false,
# which terminates the loop and closes the window.


