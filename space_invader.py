import pygame
import sys
import random
import math


def draw_player(x, y):
    screen.blit(player, (x, y))


def draw_enemy(x, y, i):
    screen.blit(enemy[i], (x, y))


def show_score(x, y):
    s = myFont.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(s, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bullet, (x + 16, y + 10))


def explosion(enemy_x, enemy_y, bullet_x, bullet_y):
    global bullet_state
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27 and bullet_state == "fired":
        return True
    return False


def set_level(score):
    global num_of_enemies, enemy, enemy_x, enemy_y, enemy_changex, enemy_changey
    if score % 15 == 0:
        enemy.append(pygame.image.load('asteroid.png'))
        enemy_x.append(random.randint(0, width - 64))  # 64 pixels is the size of the enemy
        enemy_y.append(random.randint(0, 100))
        enemy_changex.append(0.3)
        num_of_enemies += 1


pygame.init()

# screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
background = (5, 5, 25)

# title
pygame.display.set_caption("Space Invaders")
# icon = pygame.image.load('space-invaders.png')
# pygame.display.set_icon(icon)

# player
player = pygame.image.load('space-invaders.png')
player_x = 370
player_y = 480
step = 0
jump = 0

# enemy
enemy = []
enemy_x = []
enemy_y = []
enemy_changex = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy.append(pygame.image.load('asteroid.png'))
    enemy_x.append(random.randint(0, width - 64))  # 64 pixels is the size of the enemy
    enemy_y.append(random.randint(0, 100))
    enemy_changex.append(0.4)

enemy_changey = 40

# bullet
bullet = pygame.image.load('bullet.png')
bullet_y = player_y
bullet_x = 0
bullet_changey = 0.7
bullet_state = "ready"  # ready - means you can t see the bullet on the screen

game_over = False

# score
score = 0
myFont = pygame.font.SysFont("monospace", 35)
text_x = 10
text_y = 10

while not game_over:

    screen.fill(background)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # move left
                step = -0.2
            if event.key == pygame.K_RIGHT:  # move right
                step = 0.2
            if event.key == pygame.K_UP:
                jump = -0.1
            if event.key == pygame.K_DOWN:
                jump = 0.1
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_y = player_y
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                step = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                jump = 0

    player_x = player_x + step
    player_y = player_y + jump
    # we make sure that the player doesn t exit the screen
    if player_x <= 0:
        player_x = 0
    if player_x >= width - 64:  # 64 pixels is the size of the player
        player_x = width - 64

    if player_y <= 0:
        player_y = 0
    if player_y >= height - 64:  # 64 pixels is the size of the player
        player_y = height - 64

    for i in range(num_of_enemies):

        # game over
        if enemy_y[i] >= height-64:
            for j in range(num_of_enemies):
                enemy_y[j] = 1000
            game_over = True
            break

        enemy_x[i] += enemy_changex[i]
        if enemy_x[i] <= -64 or enemy_x[i] >= width:
            enemy_changex[i] *= -1
            enemy_y[i] += enemy_changey

        if enemy_y[i] >= height:
            enemy_y[i] = -60
        collision = explosion(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, width - 64)
            enemy_y[i] = -30
            set_level(score)
            print(num_of_enemies)

        draw_enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= -32:
        bullet_state = "ready"
        bullet_y = player_y

    if bullet_state == "fired":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_changey

    draw_player(player_x, player_y)
    show_score(text_x, text_y)

    pygame.display.update()
